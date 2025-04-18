# Generated by Django 5.1.3 on 2025-02-28 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import datasources.encoders


class Migration(migrations.Migration):

    dependencies = [
        ("datasources", "0008_datasource_schema"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CommonDataSourceConfig",
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
                (
                    "source_type",
                    models.CharField(
                        choices=[
                            ("FILE", "🗄️ File"),
                            ("POSTGRES", "🐘 PostgreSQL"),
                            ("MYSQL", "🐬 MySQL"),
                            ("S3", "☁️ S3"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "config",
                    models.JSONField(
                        blank=True, encoder=datasources.encoders.PrettyJSONEncoder
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authored_common_data_source_configs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "users_with_access",
                    models.ManyToManyField(
                        blank=True,
                        related_name="accessible_common_data_source_configs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
