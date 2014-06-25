.. image:: https://pypip.in/v/django-mangopay/badge.png
    :target: https://crate.io/packages/django-mangopay/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/FundedByMe/django-mangopay.svg?branch=master
    :target: https://travis-ci.org/FundedByMe/django-mangopay
    :alt: Travis CI Status

|
|

Django-Mangopay is a `Django <https://www.djangoproject.com/>`_ wrapper for the
PSP `Mangopay's V2 API <http://docs.mangopay.com/api-references/>`_. It provides Django-specfic functionality around `Mangopay's Python
SDK <https://github.com/MangoPay/mangopay2-python-sdk>`_. It creates a Mangopay
Client via settings in your ``settings.py``. It provides Django Models that allow
you to persist the data that you need to send and recieve from Mangopay. These
models have functions that correspond to the Mangopay's API calls. Celery tasks
are also provided if you want to call these functions asynchronously.

Read extended documentation provided at `Read the Docs <http://django-mangopay.readthedocs.org/en/latest/>`_.
