from django.db import models
from ..encoders import PrettyJSONEncoder


class DataSample(models.Model):
    data = models.JSONField(encoder=PrettyJSONEncoder, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
