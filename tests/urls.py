# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.http import HttpResponse
from django.urls import path, include

import django_user_emulation.urls


def home_page(request):
    return HttpResponse()


urlpatterns = [
    path('', home_page),
    path('', include(django_user_emulation.urls,
                     namespace='django_user_emulation')),
]
