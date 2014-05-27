Correspondance to Mangopay Rest API
===================================

This library is a wrapper of the Mangopay API as described `here
<http://docs.mangopay.com/api-references/>`_. Each of the API calls provided
are shown with an explaination of how to use them.

Access
------

`POST /v2/oauth/token <http://docs.mangopay.com/api-references/authenticating/>`_
*********************************************************************************

The client handles authentication with a token once you have set up your client
as described in the installation instructions. Once confrigured it is easy to
get an instance of the client.

::

    import mangopay.client

    client = get_mangopay_api_client()


Activity, research & lists
--------------------------

None of the API calls listed by Mangopay as falling under the category of "Activity, research & lists" by this library supported at the moment. It is however possible to call use the mangopay-sdk to call them indirectly. An example is given below.

::

    import mangopay.client

    client = get_mangopay_api_client()
    # GET /Events
    client.events.Get()

Users
-----

`POST /users/natural <http://docs.mangopay.com/api-references/users/natural-users/>`_
*************************************************************************************

To create a natural user object just instantiate an instance of
``MangoPayNaturalUser``, populate the requried fields, and call ``create()`` on
it as shown below. You can also edit the user, just update the the values you want to change in the model and then call ``update()``.

::

    from django.contrib.auth.models import User
    from datetime import date
    from mangopay.models import MangoPayNaturalUser

    user = User.object.get(id=1)

    mangopay_user = MangoPayNaturalUser()
    mangopay_user.user = user
    mangopay_user.country_of_residence = "SE"
    mangopay_user.nationality = "US"
    mangopay_user.birthday = date(1989, 10, 20)
    mangopay_user.save()

    mangopay_user.create()

    mangopay_user.address = "Högbergsgatan 66C"
    mangopay_user.save()

    mangopay_user.update()


`POST /users/legal <http://docs.mangopay.com/api-references/users/legal-users/>`_
*********************************************************************************

Creating and editing a legal user is the same as creating a natural user except Mangopay
required different fields. Instantiate the ``MangoPayLegalUser``, populate the
required fields, and call ``create()`` or ``update()`` on it as shown below.

::

    from django.contrib.auth.models import User
    from datetime import date
    from mangopay.models import MangoPayLegalUser
    from mangopay.constants import BUSINESS

    user = User.object.get(id=1)

    mangopay_user = MangoPayLegalUser()
    mangopay_user.user = user
    mangopay_user.country_of_residence = "SE"
    mangopay_user.nationality = "US"
    mangopay_user.birthday = date(1989, 10, 20)
    mangopay_user.first_name = "Rebecca"
    mangopay_user.last_name = "Meritz"
    mangopay_user.generic_business_email = "office@fundedbyme.com"
    mangopay_user.business_name = "FundedByMe AB"
    mangopay_user.type = BUSINESS
    mangopay_user.save()

    mangopay_user.create()

    mangopay_user.headquaters_address = "Regeringsgatan 29, 111 53 Stockholm"
    mangopay_user.save()

    mangopay_user.update()


`GET /users/{user_Id} <http://docs.mangopay.com/api-references/users/>`_
************************************************************************

This call is not supported. Infomation on the about the mangopay user will
already be saved on your MangoPayUserModel when you call ``create`` and/or
``update``.

`POST /KYC/Documents <http://docs.mangopay.com/api-references/kyc/documents/>`_
*******************************************************************************

To create a mangopay document for a user just instantiate a
``MangoPayDocument``, save the user and type to the document, and the call
``create()``. If successfully created the document's status should be updated to
``CREATED`` and it should be assigned a ``mangopay_id``.
Once you have added all the pages you wanted to the document you
can ask for validation from mangopay via ``ask_for_validation()``. This should
change the status of the document to ``VALIDATION_ASKED``.

::

    from mangopay.models import MangoPayUser
    from mangopay.constants import IDENTITY_PROOF

    mangopay_user = MangoPayUser.object.get(id=1)

    mangopay_document = MangoPayDocument()
    mangopay_document.mangopay_user = mangopay_user
    mangopay_document.type = IDENTITY_PROOF
    mangopay_document.save()

    mangopay_document.create()

    # Then add a 1+ MangoPayPages to your mangopay_document

    mangopay_document.ask_for_validation()



`POST /KYC/Documents/Pages <http://docs.mangopay.com/api-references/kyc/pages/>`_
*********************************************************************************
A document can have many pages, but needs at least one. Instantiate one
``MangoPayPage`` per file and call ``create()`` on the object to create it.

::

    from mangopay.models import MangoPayPage

    document = MangoPayDocument.object.get(id=1)
    file = file("tmp/file")
    page = MangoPayPage(file=file, document=document)
    page.save()
    page.create()


In order for this call to work you need to decide were you want to store your
files. Files can either be saved to Django's default storage by setting
``MANGOPAY_PAGE_DEFAULT_STORAGE`` to ``True``, or you can configure your files to be
stored on AWS by setting AWS storage via ``S3BotoStorage``. ``AWS_MEDIA_BUCKET_NAME`` and ``AWS_MEDIA_CUSTOM_DOMAIN`` must be in your setting in this case.

`GET /KYC/Documents/{Document_Id} <http://docs.mangopay.com/api-references/kyc/documents/>`_
********************************************************************************************
One business day after asking for validation you should be able to see if mangopay approved the document or not via
``get()`` which will get the updated document from mangopay. At this point it
should either have the status of ``VALIDATED`` or ``REFUSED``.

::

    from mangopay.models import MangoPayDocument

    document = MangoPayDocument.object.get(id=1)
    document.get()


Wallets
-------

`POST /wallets`_
****************

In order create a wallet just instantiate a ``MangoPayWallet`` object, add user
to it, save it and call ``create()`` on it with a supported currency.

::

    from mangopay.models MangoPayWallet, MangoPayUser

    user = MangoPayUser.object.get(id=1)
    wallet = MangoPayWallet()
    wallet.mangopay_user = user
    wallet.save()

    wallet.create("SEK", "Sven's Wallet")


`GET /wallets/{Wallet_Id}`_
***************************

``GET`` is not supported directly, however you can call ``balance()`` on a
created ``MangoPayWallet`` to find the amount of ``Money`` on the wallet.

PayIns
------

`POST /payins/card/web`_
*********************

Not supported via this library or the API it is only supported by MangoPay's web interface.

`POST /payins/card/direct`_
***************************
Once you have successfully registered a card you can create a payin from that
card to a created wallet. Instantiate a ``MangoPayPayIn`` model, add the user,
wallet, and card; then call create with funds to be debited and optionally the
fees and the secure mode return url. The payin will be created and the
execution date, status, result code, id, status, and secure mode redirect url
will be saved to the object.

::

    from mangopay.models import (MangoPayPayIn, MangoPayCard, MangoPayWallet,
                                 MangoPayUser)

    payin = MangoPayPayIn()
    payin.mangopay_user = MangoPayUser.objects.get(id=1)
    payin.mangopay_wallet= MangoPayWallet.objects.get(id=1)
    payin.mangopay_card = MangoPayCard.objects.get(id=1)
    payin.create(debited_funds=Money(1001, "EUR"))

`POST /payins/preauthorized/direct`_
************************************

Preauthorizations are not currently supported by this library. Pull
requests welcome.

`GET /payins/{PayIn_Id}`_
*************************
Once a ``MangoPayPayIn`` is created it's associated status can be updated via
calling ``get()`` on the instance.

::

    from mangopay.models import MangoPayPayIn

    payin = MangoPayPayIn.objects.get(id=1)
    payin.get()


`POST /cardregistration`_
**************************
Before a card can be used it must be registered with a user. Just instantiate a ``MangoPayCardRegistration`` object, add a user to it, and call ``create()`` with a supported currency. When you do this MangoPay's ID will be saved to the object.

::

    from mangopay.models import MangoPayCardRegistration, MangoPayUser

    card_registration = MangoPayCardRegistration()
    card_registration.mangopay_user = MangoPayUser.object.get(id=1)
    card_registration.create("EUR")


`GET /cardregistration/{CardRegistration_Id}`_
**********************************************
Once you have created a ``MangoPayCardRegistration`` object you can
access the card's preregistration data by calling ``get_preregistration_data()``. This data comes in the form of a dictionary with the keys: "preregistrationData", "accessKey", and "cardRegistrationURL".

::

    from mangopay.models import MangoPayCardRegistration

    card_registration = MangoPayCardRegistration.objects.get(id=1)
    card_registration.get_preregistration_data()


`GET /cards/{Card_Id}`_
********************
After registering a card with MangoPay you should get back the card's Id. If you
save that card's Id to the related ``MangoPayCard`` object by calling
``save_mangopay_card_id()``, then later you can access the card's info by calling
``request_card_info()``. Requesting the card's info will save the
expiration date, alias, and active and valid state to the ``MangoPayCard``
object.

::

    from mangopay.models import MangoPayCardRegistration

    card_registration = MangoPayCardRegistration.objects.get(id=1)
    card_registration.save_mangopay_card_id("123456")

    card_registration.mangopay_card.request_card_info()


`POST /preauthorization/card/direct`_
**********************************

Preauthorizations are not currently supported by this library. Pull
requests welcome.

`GET /preauthorization/{PreAuthorization_Id}`_
*******************************************

Preauthorizations are not currently supported by this library. Pull
requests welcome.

Refunds
-------

`POST /transfers/{Transfer_Id}/Refund`_
***************************************
Transfers and refunds of those transfers are not supported by this library. Pull
requests are welcome.

`POST /payins/{PayIn_Id}/Refund`_
*********************************
Currently on simple refunds are supported. That means you can only create a
complete refund on a pay in, not a partial one. To create a simple refund just
instantiate a ``MangoPayRefund`` object and add the payin you want to refund and
the user; then save it and call ``create_simple()``. The MangoPay's Id, the
execution date, and status will be updated in the object. If the refund was
successful then ``create_simple`` will return ``True``.

::

    from mangopay.models import MangoPayRefund, MangoPayPayIn

    refund = MangoPayRefund()
    payin = MangoPayPayIn.objects.get(id=1)
    refund.payin = payin
    refund.mangopay_user = payin.mangopay_user
    refund.save()

    refund.create_simple()


`GET /refunds/{Refund_Id}`_
***************************

Getting a refund via its ID is not supported by this library. Pull requests
welcome.

PayOuts
-------

`POST /payouts/bankwire`_
*************************

Payouts can be transfer money from a wallet to a user's bank account. In order
to a payout to run successfully they correct level of user verifications but
have been completed. To use it simply instantiate the ``MangoPayPayOut`` object
add the user, the wallet you want to transfer from, and the bank account you
want to transfer to, the funds to be debited, and optionally the fees to be
taken; then save it and run ``create()``. MangoPay's
generated id, the status, and the execution date will be saved to the object.

::

    from money import Money
    from mangopay.models import MangoPayPayOut, MangoPayUser, MangoPayWallet, MangoPayBankAccount

    payout = MangoPayPayOut()
    payout.mangopay_user = MangoPayUser.object.get(id=1)
    payout.mangopay_wallet = MangoPayUser.object.get(id=1)
    payout.mangopay_bank_account = MangoPayBankAccount.object.get(id=1)
    payout.debited_funds = Money(1000, "EUR")
    payout.fees = Money(10, "EUR")
    payout.save()

    payout.create()


`GET /payouts/{PayOut_Id}`_
***************************
Getting a payout will update the status and execution date from MangoPay.

::

    from mangopay.models import MangoPayPayOut

    payout = MangoPayPayOut.object.get(id=1)
    payout.get()
