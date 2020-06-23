from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='example')),
    path('', include('django_user_emulation.urls', namespace='emulation')),
]
