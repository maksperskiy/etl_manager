import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_celery_beat.models import (ClockedSchedule, CrontabSchedule,
                                       IntervalSchedule, PeriodicTask,
                                       SolarSchedule)

from .periodic_task import ManagerRunPeriodicTask


class DataManager(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="authored_data_managers",
    )
    users_with_access = models.ManyToManyField(
        User, blank=True, related_name="accessible_data_managers"
    )

    source = models.ForeignKey(
        "datasources.DataSource",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="datamanagers",
    )
    builder = models.ForeignKey(
        "databuilders.DataBuilder",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="datamanagers",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        crontab, _ = CrontabSchedule.objects.get_or_create(day_of_month=1)
        task = ManagerRunPeriodicTask.objects.get_or_create(
            datamanager=self,
            defaults=dict(
                name=f"task_for_{self.id}",
                task="datamanagers.tasks.run_process",
                args=f"[{self.id}]",
                crontab=crontab,
                enabled=False,
            ),
        )
