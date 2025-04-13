# Generated by Django 5.1.3 on 2025-03-01 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import databuilders.encoders


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("datasources", "0009_commondatasourceconfig"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DataBuilder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "config",
                    models.JSONField(
                        blank=True, encoder=databuilders.encoders.PrettyJSONEncoder
                    ),
                ),
                (
                    "schema",
                    models.JSONField(
                        blank=True,
                        encoder=databuilders.encoders.PrettyJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authored_data_builders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "databuilders",
                    models.ManyToManyField(
                        blank=True,
                        related_name="uses_databuilders",
                        to="databuilders.databuilder",
                    ),
                ),
                (
                    "datasources",
                    models.ManyToManyField(
                        blank=True,
                        related_name="uses_databuilders",
                        to="datasources.datasource",
                    ),
                ),
                (
                    "users_with_access",
                    models.ManyToManyField(
                        blank=True,
                        related_name="accessible_data_builders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
