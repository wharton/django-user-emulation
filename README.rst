=====================
DEPRECATED: django-user-emulation
=====================
Installable app enabling emulation of another user

.. important::

   This project is no longer maintained. The repository will remain available in a read-only mode, but we are no longer accepting pull requests or addressing issues.

What This Means
===============

- The code is provided *as-is*, and can still be used and forked, but is no longer being actively developed.
- We will not be adding new features, fixing non-critical bugs, or responding to questions.
- No additional releases will be made.

Archive Notice
==============

On 11/13/2023, this project was officially archived. For historical purposes, the source is still available, but we encourage you to find alternatives that support recent updates and active development.


Documentation
-------------

* TODO

Quickstart
----------

Install django-user-emulation::

    pip install git+https://github.com/wharton/django-user-emulation.git

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        ...
        'django_user_emulation.apps.DjangoUserEmulationConfig',
        ...
    )

Add middleware processor 'django_user_emulation.middleware.EmulationRemoteUserMiddleware',
App must also include 3 middleware from django.contrib.auth.middleware 
    AuthenticationMiddleware, RemoteUserMiddleware and SessionAuthenticationMiddleware
django_user_emulation middleware must be between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' 

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_user_emulation.middleware.EmulationRemoteUserMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        ...
    )

Add context processor

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': ...,
            'DIRS':...,.
            'OPTIONS': {
                'context_processors': [
                    "django.contrib.auth.context_processors.auth",
                    ...
                    "django_user_emulation.context_processors.emulation",
                    ...
                ]
            }
        }
    ]

Add django-user-emulation's URL patterns:

.. code-block:: python

    from django_user_emulation import urls as django_user_emulation_urls


    urlpatterns = [
        ...
        url(r'^', include(django_user_emulation_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
