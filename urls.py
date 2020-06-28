from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^world/', include('geo_django.world.urls'), name='world'),
]