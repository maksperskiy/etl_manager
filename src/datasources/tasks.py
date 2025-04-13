from celery import shared_task
from django.apps import apps


@shared_task
def refresh_schema(source_pk: int):
    DataSourceModel = apps.get_model(app_label="datasources", model_name="DataSource")

    source = DataSourceModel.objects.get(pk=source_pk)
    source.set_schema()
