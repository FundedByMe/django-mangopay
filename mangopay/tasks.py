from datetime import datetime, timedelta

from django.conf import settings

from celery.task import task
from celery.task import PeriodicTask
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from mangopaysdk.types.exceptions.responseexception import ResponseException

from .constants import VALIDATION_ASKED
from .models import (MangoPayUser, MangoPayBankAccount,
                     MangoPayDocument, MangoPayWallet, MangoPayPayOut,
                     MangoPayTransfer)

logger = get_task_logger(__name__)


def next_weekday():
    def maybe_add_day(date):
        if datetime.weekday(date) >= 5:
            date += timedelta(days=1)
            return maybe_add_day(date)
        else:
            return date
    return maybe_add_day(datetime.now() + timedelta(days=1))


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


@task
def update_document_status(id):
    document = MangoPayDocument.objects.get(id=id)
    if document.status == VALIDATION_ASKED:
        document.get()


class UpdateDocumentsStatus(PeriodicTask):
    abstract = True
    run_every = crontab(minute=0, hour='8-17', day_of_week='mon-fri')

    def run(self, *args, **kwargs):
        documents = MangoPayDocument.objects.filter(status=VALIDATION_ASKED)
        for document in documents:
            update_document_status.delay(document.id)


@task
def create_mangopay_wallet(id, description):
    wallet = MangoPayWallet.objects.get(id=id, mangopay_id__isnull=True)
    try:
        wallet.create(description=description)
    except ResponseException as exc:
        kwargs = {"id": id, "description": description}
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
    elif payout.status == "SUCCEEDED":
        task = getattr(settings, 'MANGOPAY_PAYOUT_SUCCEEDED_TASK', None)
        if task:
            task().run(payout_id=payout.id)
    else:
        logger.error("Payout %i could not be processed successfully" % payout.id)

@task
def create_mangopay_transfer(transfer_id, fees=None):
    transfer = MangoPayTransfer.objects.get(id=transfer_id)
    try:
        transfer.create(fees=fees)
    except ResponseException, e:
        kwargs = {"transfer_id": transfer_id, "fees": fees}
        raise create_mangopay_transfer.retry((), kwargs, exc=e)
