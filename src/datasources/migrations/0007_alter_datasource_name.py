# Generated by Django 5.1.3 on 2025-02-07 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datasources", "0006_alter_datasource_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasource",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
