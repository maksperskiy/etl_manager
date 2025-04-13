from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask


class ManagerRunPeriodicTask(PeriodicTask):
    datamanager = models.OneToOneField(
        "datamanagers.DataManager", on_delete=models.CASCADE, null=True, blank=True
    )
