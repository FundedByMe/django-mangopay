django-mangopay
===============

[![Downloads](https://pypip.in/v/django-mangopay/badge.png)](https://pypi.python.org/pypi/django-mangopay)
[![Build Status](https://travis-ci.org/FundedByMe/django-mangopay.svg?branch=master)](https://travis-ci.org/FundedByMe/django-mangopay)

Django Wrapper for Mangopay


Installation
============

1. Install package from PyPI:

    pip install django-mangopay


1. [Create a test client](https://github.com/MangoPay/mangopay2-python-sdk#client-creation-example-you-need-to-call-it-only-once)

1. Add your newly created client id and password to your django settings.

Example
=======

    from mangopay.client import get_mangopay_api_client
    client = get_mangopay_api_client()
    client.users.GetAll()
    [<mangopaysdk.entities.usernatural.UserNatural object at 0x5e33c50>]

Settings
========

`django.conf.settings.MANGOPAY_CLIENT_ID`

The client id you made up when you created your mangopay account.

`django.conf.settings.MANGOPAY_PASSPHRASE`

The passphase you recieved when you set up your client.

`django.conf.settings.MANGOPAY_DEBUG_MODE`

0 or 1