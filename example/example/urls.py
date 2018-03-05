from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('app.urls', namespace='example')),
    url(r'^', include('django_user_emulation.urls', namespace='emulation')),
]
