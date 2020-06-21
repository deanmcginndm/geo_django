from django.contrib import admin

# Register your models here.

from django.contrib.gis import admin
from .models import WorldBorder, CountryDivision
from leaflet.admin import LeafletGeoAdmin

admin.site.register(WorldBorder, LeafletGeoAdmin)
admin.site.register(CountryDivision, LeafletGeoAdmin)
