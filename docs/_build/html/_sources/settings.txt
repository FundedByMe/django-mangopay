Settings
========

.. _settings_client_id:

``MANGOPAY_CLIENT_ID``
----------------------

The client id you made up when you created your mangopay account.

.. _settings_passpharse:

``MANGOPAY_PASSPHRASE``
-----------------------

The passphase you recieved when you set up your client.

.. _setting_base_url:

``MANGOPAY_BASE_URL``
---------------------

Set to https://api.mangopay.com in production and https://api.sandbox.mangopay.com for testing.


``MANGOPAY_DEBUG_MODE``
-----------------------

0 or 1

.. _settings_page_default_storage:

``MANGOPAY_PAGE_DEFAULT_STORAGE``
---------------------------------

Set this to ``True`` if you want ``MangoPayPage`` files to be stored in the
default storage. Otherwise you need to have S3BotoStorage set up and working
correctly to store the files on AWS.
