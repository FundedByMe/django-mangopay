Django-Mangopay is a `Django <https://www.djangoproject.com/>`_ wrapper for `Mangopay V2 <http://www.mangopay.com/>`_. There is already a
Mangopay provides an SDK for calling their API via python. This package extends
this functionality so that you can create and save Django Models with the data
you need to send a recieve from Mangopay. These


.. image:: https://pypip.in/v/django-mangopay/badge.png
    :target: https://crate.io/packages/django-mangopay/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/FundedByMe/django-mangopay.svg?branch=master
    :target: https://travis-ci.org/FundedByMe/django-mangopay
    :alt: Travis CI Status


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
