# Generated by Django 5.1.3 on 2025-02-05 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0005_alter_datasource_config_alter_datasource_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
