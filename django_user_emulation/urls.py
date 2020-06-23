from django.urls import path
from django_user_emulation import views

app_name = "emulation"

urlpatterns = [
    path('start/', views.EmulateView.as_view(), name='emulate-start'),
    path('end/', views.EmulateEndView.as_view(), name='emulate-end'),
]
