from celery import shared_task
from django.apps import apps

@shared_task
def set_sample(builder_pk: int, size: int):
    DataBuilderModel = apps.get_model(app_label='databuilders', model_name='DataBuilder')
    DataSampleModel = apps.get_model(app_label='databuilders', model_name='DataSample')

    builder = DataBuilderModel.objects.get(pk=builder_pk)
    builder.sample = DataSampleModel.objects.create()
    builder.save()

    df = builder.build_dataframe().limit(size)
    headers = df.columns
    rows = df.collect()
    data =  {"headers": headers, "data": [list(row) for row in rows]}
    builder.sample.data = data
    builder.sample.save()