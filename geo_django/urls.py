from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^world/', include('world.urls')),
    url('admin/', admin.site.urls),
]