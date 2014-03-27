from celery.task import task

from .models import MangoPayNaturalUser


@task
def create_mangopay_natural_user(id):
    MangoPayNaturalUser.objects.get(id=id, mangopay_id__isnull=True).create()
