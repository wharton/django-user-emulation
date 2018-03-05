from django.conf.urls import url
from example import views


urlpatterns = [
    url(r'^emulate/$', views.EmulateView.as_view(), name='emulate'),
    url(r'^autocomplete/$', views.AutocompleteView.as_view()),
]