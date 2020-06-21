from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import WorldBorder, CountryDivision
import time


class GenericMapListView(generic.ListView):

    def __init__(self):
        super(GenericMapListView, self).__init__()

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Override context data to include the geometry json
        """
        data = super(GenericMapListView, self).get_context_data(object_list=self.model.objects.all(), **kwargs)
        data['geometry_list'] = [
            obj.geojson for obj in data['object_list']
        ]
        return data


class CountryDetailView(generic.DetailView):
    """
        Country Region detail view.
    """
    template_name = 'world/country-detail.html'
    model = WorldBorder


class CountryListView(generic.ListView):
    """
        Country Region detail view.
    """
    template_name = 'world/country-list.html'
    model = WorldBorder


class CountryDivisionDetailView(generic.DetailView):
    """
        Country Region detail view.
    """
    template_name = 'world/division-detail.html'
    model = CountryDivision


class CountryDivisionListView(GenericMapListView):
    """
        Country Region detail view.
    """
    template_name = 'world/division-list.html'
    model = CountryDivision

