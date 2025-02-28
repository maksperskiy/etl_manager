from django.contrib.auth.models import User
from django.db import models

from datasources.encoders import PrettyJSONEncoder
from .datasource import DataSourceType


class CommonDataSourceConfig(models.Model):
    source_type = models.CharField(
        max_length=50, blank=False, choices=DataSourceType.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    config = models.JSONField(encoder=PrettyJSONEncoder, blank=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="authored_common_data_source_configs",
    )
    users_with_access = models.ManyToManyField(
        User, blank=True, related_name="accessible_common_data_source_configs"
    )

    def __str__(self):
        return f"{self.source_type} - {self.author} - {self.created_at}"
