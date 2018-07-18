# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include

import django_user_emulation.urls

urlpatterns = [
    path('', include(django_user_emulation.urls, namespace='django_user_emulation')),
]
