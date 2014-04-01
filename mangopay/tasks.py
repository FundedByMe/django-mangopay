from celery.task import task

from .models import MangoPayNaturalUser, MangoPayBankAccount, MangoPayDocument


@task
def create_mangopay_natural_user(id):
    MangoPayNaturalUser.objects.get(id=id, mangopay_id__isnull=True).create()


@task
def update_mangopay_natural_user(id):
    MangoPayNaturalUser.objects.get(id=id, mangopay_id__isnull=False).update()


@task
def create_mangopay_bank_account(id):
    MangoPayBankAccount.objects.get(id=id, mangopay_id__isnull=True).create()


@task
def create_mangopay_document_and_page_and_ask_for_validation(id):
    document = MangoPayDocument.objects.get(
        id=id, mangopay_id__isnull=True, file__isnull=False,
        type__isnull=False)
    document.create()
    document.create_page()
    document.ask_for_validation()
