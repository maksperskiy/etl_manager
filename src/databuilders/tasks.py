from celery import Task, shared_task, states
from django.apps import apps


@shared_task(bind=True)
def refresh_schema(self: Task, builder_pk: int):
    if self.request.id:
        self.update_state(
            state=states.STARTED, meta={"stage": "Starting refresh schema."}
        )
    DataBuilderModel = apps.get_model(
        app_label="databuilders", model_name="DataBuilder"
    )
    builder = DataBuilderModel.objects.get(pk=builder_pk)
    if self.request.id:
        self.update_state(state="PROGRESS", meta={"stage": "Setting the schema."})
    try:
        builder.set_schema()
    except Exception as e:
        raise e
    finally:
        builder.clean_refresh_schema_task_id()


@shared_task(bind=True)
def set_sample(self: Task, builder_pk: int, size: int):
    self.update_state(state=states.STARTED, meta={"stage": "Starting set sample."})
    DataBuilderModel = apps.get_model(
        app_label="databuilders", model_name="DataBuilder"
    )
    DataSampleModel = apps.get_model(app_label="databuilders", model_name="DataSample")

    builder = DataBuilderModel.objects.get(pk=builder_pk)
    if builder.sample:
        builder.sample.delete()
    builder.save()
    self.update_state(state="PROGRESS", meta={"stage": "Refreshing schema."})

    try:
        refresh_schema(builder_pk)

        self.update_state(state="PROGRESS", meta={"stage": "Building sample."})

        df = builder.build_dataframe().limit(size)

        headers = df.columns
        rows = df.collect()

        self.update_state(state="PROGRESS", meta={"stage": "Saving sample."})

        data = {"headers": headers, "data": [list(row) for row in rows]}
    except Exception as e:
        raise e
    finally:
        builder.clean_refresh_sample_task_id()
    builder.sample = DataSampleModel.objects.create()
    builder.save()
    builder.sample.data = data
    builder.sample.save()
