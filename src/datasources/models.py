from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .encoders import PrettyJSONEncoder

class DataSourceType(models.TextChoices):
    FILE = 'FILE', '🗄️ File'
    POSTGRES = 'POSTGRES', '🐘 PostgreSQL'
    MYSQL = 'MYSQL', '🐬 MySQL'
    S3 = 'S3', '☁️ S3'

class DataSource(models.Model):
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, choices=DataSourceType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    config = models.JSONField(encoder=PrettyJSONEncoder, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='authored_data_sources')
    users_with_access = models.ManyToManyField(User, blank=True, related_name='accessible_data_sources')
    upload = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_connection(self):
        from .connectors import DataSourceConnector
        connector = DataSourceConnector(self)
        return connector.connect()
