from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from app import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/$', auth_views.login,
         {'template_name': 'login.html'}, name='login'),
    path('logout/$', auth_views.logout,
         {'template_name': 'logged_out.html', 'extra_context': {'next': '/'}}, name='logout'),
    path('emulate/$', views.EmulateView.as_view(), name='emulate'),
    path('autocomplete/$', views.AutocompleteView.as_view(),
         name='autocomplete-users'),
]
