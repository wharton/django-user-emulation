from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from app import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'logged_out.html', 'extra_context': {'next': '/'}}, name='logout'),
    url(r'^emulate/$', views.EmulateView.as_view(), name='emulate'),
    url(r'^autocomplete/$', views.AutocompleteView.as_view(), name='autocomplete-users'),
]
