Tasks
=====

Celery tasks are provided. If desired you may use them to asynchcroniously call
the MangoPay API.

create_mangopay_user
--------------------

Takes the id of a ``MangoPayUser`` and creates it. See :ref:`post_users_natural` and :ref:`post_users_legal`.

::

    from django.contrib.auth.models import User
    from datetime import date
    from mangopay.models import MangoPayNaturalUser
    from mangopay.tasks import create_mangopay_user

    user = User.objects.get(id=1)

    mangopay_user = MangoPayNaturalUser()
    mangopay_user.user = user
    mangopay_user.country_of_residence = "SE"
    mangopay_user.nationality = "US"
    mangopay_user.birthday = date(1989, 10, 20)
    mangopay_user.save()

    create_mangopay_user.delay(id=mangopay_user.id)


update_mangopay_user
--------------------

Takes the id of a ``MangoPayUser`` and updates it. See :ref:`post_users_natural` and :ref:`post_users_legal`.

create_mangopay_bank_account
----------------------------

Takes the id of a ``MangoPayBankAccount`` and creates it. See :ref:`post_user_bank_account`.

create_mangopay_document_and_pages_and_ask_for_validation
---------------------------------------------------------

Takes the id of a ``MangoPayDocument`` creates the document and all the related
pages and then asks for validation of the document. Runs
``update_document_status`` the following weekday. MangoPay says they will verify
and update the status of your document the following business day. See
:ref:`post_kyc_documents`.

update_document_status
----------------------

Takes the id of a ``MangoPayDocument`` and updates the status of it. The task will
call itself again the next weekday if the document still has the status
``VALIDATION_ASKED``. See :ref:`get_kyc_documents`.

create_mangopay_wallet
----------------------

Takes the id of a ``MangoPayWallet`` and creates it. See :ref:`post_wallets`.

create_mangopay_pay_out
-----------------------

Takes the id of a ``MangoPayPayOut`` and creates it. See
:ref:`post_payouts_bankwire`.

update_mangopay_pay_out
-----------------------

Takes the id of a ``MangoPayPayOut`` and updates it. If it still has the status
"CREATED" it will be run again the following weekday. See :ref:`get_payouts`.
