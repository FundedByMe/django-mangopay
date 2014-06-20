Tasks
=====

Celery tasks are provided. If desired you may use them to asynchcroniously call
the MangoPay API.

create_mangopay_user
--------------------

Takes the id of a ``MangoPayUser`` and creates it.

update_mangopay_user
--------------------

Takes the id of a ``MangoPayUser`` and updates it.

create_mangopay_bank_account
----------------------------

Takes the id of a ``MangoPayBankAccount`` and creates it.

create_mangopay_document_and_pages_and_ask_for_validation
---------------------------------------------------------

Takes the id of a ``MangoPayDocument`` creates the document and all the related
pages and then asks for validation of the document. Runs
``update_document_status`` the following weekday. MangoPay says they will verify
and update the status of your document the following business day.

update_document_status
----------------------

Takes the id of a ``MangoPayDocument`` and updates the status of it. The task will
call itself again the next weekday if document still has the status
"VALIDATION_ASKED".

create_mangopay_wallet
----------------------

Takes the id of a ``MangoPayWallet`` and creates it.

create_mangopay_pay_out
-----------------------

Takes the id of a ``MangoPayPayOut`` and creates it.

update_mangopay_pay_out
-----------------------

Takes the id of a ``MangoPayPayOut`` and updates it. If its still has the status
"CREATED" it will be run again the following weekday.
