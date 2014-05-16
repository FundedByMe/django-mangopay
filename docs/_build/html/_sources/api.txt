Correspondance to Mangopay Rest API
===================================

This library is a wrapper of the Mangopay API as described `here
<http://docs.mangopay.com/api-references/>`_. This page goes through each of
Mangopay's API calls and described the corresponding call in this library and the
corresponding `entity
<https://github.com/MangoPay/mangopay2-python-sdk/tree/master/mangopaysdk/entities>`_
provided from the  mangopay2-python-sdk.

Access
------

POST /v2/oauth/token
********************

The client handles authentication with a token once you have set up your client
as described in the installation instructions. Once confrigured it is easy to
get an instance of it to contect to.

::
    import mangopay.client

    client = get_mangopay_api_client()


Activity, research & lists
--------------------------

None of the API calls listed by Mangopay as falling under the category of "Activity, research & lists" are supported at the moment. It is however possible to call use the mangopay-sdk to call them indirectly. An example is given below.

::
    import mangopay.client

    client = get_mangopay_api_client()
    # GET /Events
    client.events.Get()

Users
-----

All API calls under the "Users" are supported.

`POST /users/natural <http://docs.mangopay.com/api-references/users/natural-users/>`_
*************************************************************************************

To create a natural user object just instantiate an instance of
``MangoPayNaturalUser``, populate the requried fields, and call ``create()`` on
it as shown below.

::
    from django.contrib.auth.models import User
    from datetime import date
    import mangopay.models

    user = User.object.get(id=1)

    mangopay_user = MangoPayNaturalUser()
    mangopay_user.user = user
    mangopay_user.country_of_residence = "SE"
    mangopay_user.nationality = "US"
    mangopay_user.birthday = date(1989, 10, 20)
    mangopay_user.save()

    mangopay_user.create()


Wallets
-------

MangoPayWallet

PayIns
------

MangoPayBankAccount
MangoPayPayOut
MangoPayCard
MangoPayCardRegistration
MangoPayPayIn
MangoPayRefund
