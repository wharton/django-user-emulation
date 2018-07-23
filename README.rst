=============================
django-user-emulation
=============================

Installable app enabling emulation of another user

Documentation
-------------

* TODO

Quickstart
----------

Install django-user-emulation::

    pip install git+https://github.com/wharton/django-user-emulation.git

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django.contrib.auth',
        ...
        'django_user_emulation.apps.DjangoUserEmulationConfig',
        ...
    ]

Add middleware processor 'django_user_emulation.middleware.EmulationRemoteUserMiddleware',
App must also include middleware from django.contrib.auth.middleware 
    AuthenticationMiddleware, RemoteUserMiddleware or your custom remote user middleware (such as shibboleth)
django_user_emulation middleware must be between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' 
because it overrides the REMOTE_USER request header which sets the user in RemoteUserMiddleware

.. code-block:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_user_emulation.middleware.EmulationRemoteUserMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        ...
    ]

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
        path('', include(django_user_emulation_urls)),
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
