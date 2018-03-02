=====
Usage
=====

To use django-user-emulation in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_user_emulation.apps.DjangoUserEmulationConfig',
        ...
    )

Add django-user-emulation's URL patterns:

.. code-block:: python

    from django_user_emulation import urls as django_user_emulation_urls


    urlpatterns = [
        ...
        url(r'^', include(django_user_emulation_urls)),
        ...
    ]
