.. image:: https://pypip.in/v/django-mangopay/badge.png
    :target: https://crate.io/packages/django-mangopay/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/FundedByMe/django-mangopay.svg?branch=master
    :target: https://travis-ci.org/FundedByMe/django-mangopay
    :alt: Travis CI Status

|
|

Django-Mangopay is a `Django <https://www.djangoproject.com/>`_ wrapper for the
PSP `Mangopay's V2 API <http://docs.mangopay.com/api-references/>`_. More
specifically it provides Django-specfic functionality around `Mangopay's Python
SDK <https://github.com/MangoPay/mangopay2-python-sdk>`_. It creates a Mangopay
Client via settings in your ``settings.py``. It provides Django Models that allow
you to persist the data that you need to send and recieve from Mangopay. These
models have functions that correspond to the Mangopay's API calls. Celery tasks
are also provided if you want to call these functions asynchronously. Read
extended documentation is provide at `Read the Docs <http://django-mangopay.readthedocs.org/en/latest/>`_.

Installation
============

1. Install package from PyPI:

::

    pip install django-mangopay


2. `Create a test client <https://github.com/MangoPay/mangopay2-python-sdk#client-creation-example-you-need-to-call-it-only-once>`_

3. Add your newly created client id and password to your django settings.


Example
=======

::

    from mangopay.client import get_mangopay_api_client
    client = get_mangopay_api_client()
    client.users.GetAll()
    [<mangopaysdk.entities.usernatural.UserNatural object at 0x5e33c50>]

Settings
========

``django.conf.settings.MANGOPAY_CLIENT_ID``

The client id you made up when you created your mangopay account.

``django.conf.settings.MANGOPAY_PASSPHRASE``

The passphase you recieved when you set up your client.

``django.conf.settings.MANGOPAY_DEBUG_MODE``

0 or 1
