from datetime import datetime, timedelta

from celery.task import task

from .constants import VALIDATION_ASKED
from .models import (MangoPayUser, MangoPayBankAccount,
                     MangoPayDocument, MangoPayWallet, MangoPayPayOut)


@task
def create_mangopay_user(id):
    MangoPayUser.objects.select_subclasses().get(
        id=id, mangopay_id__isnull=True).create()


@task
def update_mangopay_user(id):
    MangoPayUser.objects.select_subclasses().get(
        id=id, mangopay_id__isnull=False).update()


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


def next_weekday():
    def maybe_add_day(date):
        if datetime.weekday(date) > 6:
            date = date + timedelta(days=1)
            return maybe_add_day(date)
        else:
            return date


@task
def update_document_status(id):
    document = MangoPayDocument.objects.get(id=id, status=VALIDATION_ASKED)
    updated_document = document.get()
    if updated_document.status == VALIDATION_ASKED:
        eta = next_weekday()
        update_document_status.apply_async({id: id}, eta=eta)


@task
def create_mangopay_wallet(id, currency, description=""):
    wallet = MangoPayWallet.objects.get(id=id, mangopay_id__isnull=True)
    wallet.create(currency=currency, description=description)


@task
def create_mangopay_pay_out(id, debited_funds=None, fees=None, tag=''):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=True)
    payout.create()
