from celery.task import task

from .models import MangoPayNaturalUser, MangoPayBankAccount


@task
def create_mangopay_natural_user(id):
    MangoPayNaturalUser.objects.get(id=id, mangopay_id__isnull=True).create()


@task
def update_mangopay_natural_user(id):
    MangoPayNaturalUser.objects.get(id=id, mangopay_id__isnull=False).update()


@task
def create_mangopay_bank_account(id):
    MangoPayBankAccount.objects.get(id=id, mangopay_id__isnull=True).create()
