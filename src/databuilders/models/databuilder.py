import json
import logging
from datetime import datetime, timedelta, timezone

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from pyspark.sql import SparkSession

from databuilders.builder import ETLPipeline

from ..encoders import PrettyJSONEncoder
from ..tasks import refresh_schema as refresh_schema_
from ..tasks import set_sample
from .sample import DataSample

logger = logging.getLogger(__name__)


class DataBuilder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    config = models.JSONField(encoder=PrettyJSONEncoder, blank=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="authored_data_builders",
    )
    users_with_access = models.ManyToManyField(
        User, blank=True, related_name="accessible_data_builders"
    )
    refresh_schema_task_id = models.UUIDField(null=True)
    schema = models.JSONField(encoder=PrettyJSONEncoder, blank=True, null=True)

    datasources = models.ManyToManyField(
        "datasources.DataSource", blank=True, related_name="uses_databuilders"
    )
    databuilders = models.ManyToManyField("self", blank=True)

    refresh_sample_task_id = models.UUIDField(null=True)
    sample = models.OneToOneField(
        DataSample, blank=True, null=True, on_delete=models.SET_NULL
    )

    @property
    def spark_session_builder(self):
        return SparkSession.builder.master(settings.SPARK_MASTER_URL).appName(
            f"{self.name}-{self.id}"
        )

    def __str__(self):
        return self.name

    def combine_configs(self):
        """
        Combines all configs from the current DataBuilder and its related databuilders,
        ordered by depth (deepest first).
        """

        def collect_configs(databuilder, depth=0):
            # Recursively collect configs and their depth
            configs = []
            for related_databuilder in databuilder.databuilders.all():
                configs.extend(collect_configs(related_databuilder, depth + 1))
            configs.append(
                {"config": databuilder.config.get("transform", []), "depth": depth}
            )
            return configs

        # Collect all configs with their depth
        all_configs = collect_configs(self)

        # Sort configs by depth in descending order (deepest first)
        all_configs.sort(key=lambda x: x["depth"], reverse=True)

        # Combine the configs into a single list
        combined_config = []
        for item in all_configs:
            combined_config.extend(item["config"])

        return combined_config

    def get_related_datasources(self):
        unique_datasources = set()

        databuilders_to_process = [self]

        processed_databuilders = set()

        while databuilders_to_process:
            current_databuilder = databuilders_to_process.pop()
            if current_databuilder.id in processed_databuilders:
                continue
            processed_databuilders.add(current_databuilder.id)

            unique_datasources.update(current_databuilder.datasources.all())
            databuilders_to_process.extend(current_databuilder.databuilders.all())

        return {
            source.name: source.get_connection(self.spark_session_builder)
            for source in unique_datasources
        }

    def build_dataframe(self):
        pipeline = ETLPipeline(
            config=self.combine_configs(),
            input_dataframes=self.get_related_datasources(),
            spark_session_builder=self.spark_session_builder,
            result_df_name=self.name,
        )
        return pipeline.run()

    def get_dataframe_head(self, size: int = 10):
        if not self.sample or (self.sample.created_at < self.updated_at):
            if self.refresh_sample_task_id:
                task = AsyncResult(str(self.refresh_sample_task_id).encode())
                return dict(
                    status="refresh_running",
                    task_id=self.refresh_sample_task_id,
                    task_status=task.status,
                    task_info=task.info,
                    data=None,
                )

            task = set_sample.apply_async(
                args=(self.pk, size), soft_time_limit=60 * 1, time_limit=60 * 10
            )
            self.refresh_sample_task_id = task.id
            self.save()
            return dict(
                status="refresh_started",
                task_id=self.refresh_sample_task_id,
                task_status="PENDING",
                task_info={},
                data=None,
            )
        return dict(status="ok", data=self.sample.data)

    def clean_refresh_sample_task_id(self):
        self.refresh_sample_task_id = None
        self.save()

    def set_schema(self):
        self.schema = json.loads(self.build_dataframe().schema.json())
        self.save()
        return self.schema

    def refresh_schema(self):
        if self.refresh_schema_task_id:
            task = AsyncResult(str(self.refresh_schema_task_id).encode())
            return dict(
                status="refresh_running",
                task_id=self.refresh_schema_task_id,
                task_status=task.status,
                task_info=task.info,
            )

        task = refresh_schema_.apply_async(
            args=(self.pk,), soft_time_limit=60 * 2, time_limit=60 * 10
        )
        self.refresh_schema_task_id = task.id
        self.save()
        return dict(
            status="refresh_started",
            task_id=self.refresh_schema_task_id,
            task_status="PENDING",
            task_info={},
        )

    def clean_refresh_schema_task_id(self):
        self.refresh_schema_task_id = None
        self.save()
