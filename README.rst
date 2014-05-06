django-shareddb
===============

This proxy database backend is designed to speed up multi-threaded testing setups.

It enables those setups (for instance using ``LiveServerTestCase``) to use Django's
standard ``TestCase`` - where each test runs in its own transaction -
instead of the much slower ``TransactionTestCase`` that needs to flush the whole
database between each tests.


It is **NOT** intended for production use, only for faster testing setups.


This project support Django versions 1.6, and Python 2.7, 3.2 and 3.3.

Setup
-----

First, install django-shareddb:

.. code-block:: shel

    $ pip install django-shareddb


Then, simply update your settings to use its wrapping engine:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'shareddb.backends.shareddb',
            'INNER_ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test-dbsharing',
        }
    }

Since altering those settings is very frequent, django-shareddb also provides
a simple ``patch_databases`` function:
    
.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test-dbsharing',
        }
    }

    if os.environ['FAST_TESTS']:
        import shareddb
        DATABASES = shareddb.patch_databases(DATABASES)
    
.. note:: ``patch_databases`` accepts two keyword arguments,
          ``whitelist`` (only alter databases from that list) and
          ``blacklist`` (never alter databases from that list).

          The ``blacklist`` has priority over the ``whitelist``.


Once the settings are ready, simply replace your calls to Django's LiveServerTestCase with the django-shareddb variant:

.. code-block:: python

    from shareddb import testcases

    class MyTests(testcases.LiveServerTestCase):
        def test_something(self):
            # Your test here


The django-shareddb ``LiveServerTestCase`` is simply a clone of Django's version,
but uses ``django.test.TestCase`` instead of ``django.test.TransactionTestCase``.


Links
-----

* The code of this project is available on GitHub: https://github.com/rbarrois/django-shareddb
* It is available on PyPI: https://pypi.python.org/pypi/django-shareddb
* Issues, questions, and new features should be opened on GitHub: https://github.com/rbarrois/django-shareddb/issues


Testing
-------

This libraries has been succesfully tested with sqlite and postgresql.

If you want to test it with other databases, please clone it and alter
``dev/settings.py`` for your setup, then run ``./manage.py test``.
