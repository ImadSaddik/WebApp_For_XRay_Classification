from django.contrib import admin
from django.urls import path, include
from django.contrib.sites.models import Site

site = Site.objects.get_current()
site.domain = 'localhost:8080'
site.save()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/', include('database_handler.urls')),
    path('api/v1/', include('dl_model.urls')),
]
