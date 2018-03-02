# -*- coding: utf-8
from django.apps import AppConfig


class DjangoUserEmulationConfig(AppConfig):
    name = 'django_user_emulation'
    verbose_name = 'Django User Emulation'

    def ready(self):
        from . import signals
