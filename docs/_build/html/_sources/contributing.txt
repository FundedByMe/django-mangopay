.. _contributing:

Contributing
============

We welcome your contribution.

Please report issues via `Githubs Issue tracker <https://github.com/FundedByMe/django-mangopay/issues>`_.

Please `submit pull requests here <https://github.com/FundedByMe/django-mangopay/pulls>`_. All pull requests should include tests. Tests should not touch Mangopay's sandbox only the ``MockMangoPayApi`` in ``tests/client.py``. You must however manually insure all functionatlity works against Mangopay's sandbox.

To run the tests you will need to install the all requirements including the
test specfic ones and then run the test runner.

::

    pip install -r requirements.txt
    pip install -r requirements_test.txt

    ./run_tests.py
