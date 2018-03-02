# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_user_emulation.urls import urlpatterns as django_user_emulation_urls

urlpatterns = [
    url(r'^', include(django_user_emulation_urls, namespace='django_user_emulation')),
]
