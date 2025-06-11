from celery import Task, shared_task
from django.apps import apps


@shared_task(bind=True)
def refresh_schema(self: Task, source_pk: int):
    self.update_state(state="PROGRESS", meta={"stage": "Starting."})
    DataSourceModel = apps.get_model(app_label="datasources", model_name="DataSource")

    source = DataSourceModel.objects.get(pk=source_pk)

    self.update_state(state="PROGRESS", meta={"stage": "Setting the schema."})
    try:
        source.set_schema()
    except Exception as e:
        raise e
    finally:
        source.clean_refresh_schema_task_id()
