from datetime import datetime, timedelta

from celery.task import task
from mangopaysdk.types.exceptions.responseexception import ResponseException

from .constants import VALIDATION_ASKED
from .models import (MangoPayUser, MangoPayBankAccount,
                     MangoPayDocument, MangoPayWallet, MangoPayPayOut)


@task
def create_mangopay_user(id):
    try:
        MangoPayUser.objects.select_subclasses().get(
            id=id, mangopay_id__isnull=True).create()
    except ResponseException as exc:
        raise create_mangopay_user.retry((), {"id": id}, exc=exc)


@task
def update_mangopay_user(id):
    try:
        MangoPayUser.objects.select_subclasses().get(
            id=id, mangopay_id__isnull=False).update()
    except ResponseException as exc:
        raise update_mangopay_user.retry((), {"id": id}, exc=exc)


@task
def create_mangopay_bank_account(id):
    try:
        MangoPayBankAccount.objects.get(
            id=id, mangopay_id__isnull=True).create()
    except ResponseException as exc:
        raise create_mangopay_bank_account.retry((), {"id": id}, exc=exc)


@task
def create_mangopay_document_and_pages_and_ask_for_validation(id):
    document = MangoPayDocument.objects.get(
        id=id, mangopay_id__isnull=True, type__isnull=False)
    try:
        document.create()
    except ResponseException as exc:
        raise create_mangopay_document_and_pages_and_ask_for_validation.retry(
            (), {"id": id}, exc=exc)
    for page in document.mangopay_pages.all():
        page.create()
    document.ask_for_validation()
    eta = next_weekday()
    update_document_status.apply_async((), {"id": id}, eta=eta)


def next_weekday():
    def maybe_add_day(date):
        if datetime.weekday(date) > 6:
            date = date + timedelta(days=1)
            return maybe_add_day(date)
        else:
            return date
    return maybe_add_day(datetime.now() + timedelta(days=1))


@task
def update_document_status(id):
    document = MangoPayDocument.objects.get(id=id)
    if document.status == VALIDATION_ASKED:
        try:
            updated_document = document.get()
        except ResponseException as exc:
            raise update_document_status.retry((), {"id": id}, exc=exc)
        if updated_document.status == VALIDATION_ASKED:
            eta = next_weekday()
            update_document_status.apply_async((), {"id": id}, eta=eta)


@task
def create_mangopay_wallet(id, currency, description):
    wallet = MangoPayWallet.objects.get(id=id, mangopay_id__isnull=True)
    try:
        wallet.create(currency=currency, description=description)
    except ResponseException as exc:
        kwargs = {"id": id, "currency": currency, "description": description}
        raise create_mangopay_wallet.retry((), kwargs, exc=exc)


@task
def create_mangopay_pay_out(id, tag=''):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=True)
    try:
        payout.create(tag)
    except ResponseException as exc:
        kwargs = {"id": id, "tag": tag}
        raise create_mangopay_pay_out.retry((), kwargs, exc=exc)
    eta = next_weekday()
    update_mangopay_pay_out.apply_async((), {"id": id}, eta=eta)


@task
def update_mangopay_pay_out(id):
    payout = MangoPayPayOut.objects.get(id=id, mangopay_id__isnull=False)
    try:
        payout = payout.get()
    except ResponseException as exc:
        raise update_mangopay_pay_out.retry((), {"id": id}, exc=exc)
    if not payout.status or payout.status == "CREATED":
        eta = next_weekday()
        update_mangopay_pay_out.apply_async((), {"id": id}, eta=eta)
