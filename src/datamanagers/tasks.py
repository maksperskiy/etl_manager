from celery import shared_task
from django.apps import apps


@shared_task
def run_process(datamanager_pk: int): ...
