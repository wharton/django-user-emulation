from django.conf.urls import url
from django_user_emulation import views

urlpatterns = [
    url(r'^start$', views.EmulateView.as_view(), name='emulate-start'),
    url(r'^end$', views.EmulateEndView.as_view(), name='emulate-end'),
]
