# Generated by Django 5.1.3 on 2025-04-09 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("databuilders", "0003_datasample_databuilder_sample"),
    ]

    operations = [
        migrations.AddField(
            model_name="databuilder",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
