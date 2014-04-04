from celery.task import task

from .models import (MangoPayNaturalUser, MangoPayBankAccount,
                     MangoPayDocument, MangoPayWallet, MangoPayPayOut)


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


@task
def create_mangopay_wallet(id, currency, description=""):
    wallet = MangoPayWallet.objects.get(id=id, mangopay_id__isnull=True)
    wallet.create(currency=currency, description=description)


@task
def create_mangopay_pay_out(id, debited_funds=None, fees=None, tag=''):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=True)
    payout.create()
