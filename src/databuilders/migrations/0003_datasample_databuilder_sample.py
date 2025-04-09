# Generated by Django 5.1.3 on 2025-04-09 18:41

import databuilders.encoders
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databuilders', '0002_alter_databuilder_databuilders'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(blank=True, encoder=databuilders.encoders.PrettyJSONEncoder)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='databuilder',
            name='sample',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='databuilders.datasample'),
        ),
    ]
