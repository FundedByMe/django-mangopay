Settings
========

``django.conf.settings.MANGOPAY_CLIENT_ID``
-------------------------------------------

The client id you made up when you created your mangopay account.

``django.conf.settings.MANGOPAY_PASSPHRASE``
--------------------------------------------

The passphase you recieved when you set up your client.

``django.conf.settings.MANGOPAY_DEBUG_MODE``
--------------------------------------------

0 or 1

``django.conf.settings.MANGOPAY_PAGE_DEFAULT_STORAGE``
------------------------------------------------------

Set this to ``True`` if you want ``MangoPayPage`` files to be stored in the
default storage. Otherwise you need to have S3BotoStorage set up and working
correctly to store the files on AWS.
