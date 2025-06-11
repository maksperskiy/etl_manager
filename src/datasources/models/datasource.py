import json
import logging

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from pyspark.sql import SparkSession

from ..encoders import PrettyJSONEncoder
from ..tasks import refresh_schema as refresh_schema_

logger = logging.getLogger(__name__)


class DataSourceType(models.TextChoices):
    FILE = "FILE", "🗄️ File"
    POSTGRES = "POSTGRES", "🐘 PostgreSQL"
    MYSQL = "MYSQL", "🐬 MySQL"
    S3 = "S3", "☁️ S3"


class DataSource(models.Model):
    name = models.CharField(max_length=255, unique=True)
    source_type = models.CharField(
        max_length=50, blank=False, choices=DataSourceType.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    config = models.JSONField(encoder=PrettyJSONEncoder, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="authored_data_sources",
    )
    users_with_access = models.ManyToManyField(
        User, blank=True, related_name="accessible_data_sources"
    )
    upload = models.FileField(upload_to="uploads/", null=True, blank=True)

    refresh_schema_task_id = models.UUIDField(null=True)
    schema = models.JSONField(encoder=PrettyJSONEncoder, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def spark_session_builder(self):
        return SparkSession.builder.master(settings.SPARK_MASTER_URL).appName(
            f"{self.name}-{self.id}"
        )

    def get_connection(self, session_builder):
        from ..connectors.connector_factory import DataSourceConnectorFactory

        connector = DataSourceConnectorFactory(self)
        return connector.get_connector(session_builder=session_builder).get_dataframe()

    def set_schema(self):
        self.schema = json.loads(
            self.get_connection(self.spark_session_builder).schema.json()
        )
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
            args=(self.pk,), soft_time_limit=60 * 1, time_limit=60 * 10
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
