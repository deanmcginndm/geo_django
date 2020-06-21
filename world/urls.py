from django.conf.urls import url
from . import views


app_name = 'country'

urlpatterns = [
    url(r'^countries/$',
        views.CountryListView.as_view(), name='country-list'),
    # country detail view
    url(r'^country/(?P<slug>[-\w]+)$',
        views.CountryDetailView.as_view(), name='country-detail'),
    url(r'^country/divisions/$',
        views.CountryDivisionListView.as_view(), name='country-list'),
    url(r'^country/division/(?P<slug>[-\w]+)$',
        views.CountryDivisionDetailView.as_view(), name='division-detail'),
]