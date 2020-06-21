from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Centroid, Distance
from django.urls import reverse
from autoslug import AutoSlugField
from quantityfield import ureg
import json
from django.utils.text import slugify
from decimal import Decimal as D
Quantity = ureg.Quantity


zoom_map = {
    1: 10,
    2: 10,
    3: 6,
    4: 5,
    5: 5,
    6: 4,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 2
}


class Unit(models.Model):

    name = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=4)
    # pluralised = models.Charfield(max_length=35)
    is_canonical = models.BooleanField(default=False)


class TravelDetails(models.Model):

    _distance_value = models.DecimalField(decimal_places=12, max_digits=18, default=0)
    _distance_unit = models.ForeignKey("Unit", on_delete=models.PROTECT, blank=True, null=True)
    destination = models.ForeignKey("CountryDivision", blank=True, null=True, on_delete=models.CASCADE)

    @property
    def distance(self):
        return Quantity(self._distance_value, self._distance_unit.abbreviation)

    @distance.setter
    def distance(self, quantity):
        self._distance_unit = Unit.objects.get(name__iexact=str(quantity.units))
        self._distance_value = quantity.m

    @property
    def force_readable(self):
        return '{}'.format(str(self.distance))

    @property
    def origin(self):
        return self._origin.get()

    def __str__(self):
        return '{} >> {}, {}'.format(self.origin, self.destination, self.force_readable)


class WorldBorder(models.Model):
    zoom_map = zoom_map
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # django-autoslug field
    slug = AutoSlugField(populate_from='name')

    # Returns the string representation of the model.
    def __str__(self):
        return '{}<br>Total Area: {}<br>2005 Population: {}'.format(
            self.name, self.area, self.pop2005
        )

    @property
    def default_zoom(self):
        if self.slug == 'antarctica':
            return 1
        return self.zoom_map.get(len(str(self.area)))

    @property
    def url(self):
        return reverse('country:country-detail', args=[self.slug])


class CountryDivision(models.Model):

    zoom_map = zoom_map

    # foreign key to the border region the country division is associated to
    world_border = models.ForeignKey(
        WorldBorder, related_name='divisions', on_delete=models.PROTECT, null=True, default=None
    )

    distances = models.ManyToManyField(TravelDetails, related_name='_origin')

    # geopackage fields
    gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80)
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80)
    nl_name_1 = models.CharField(max_length=80, blank=True, null=True)
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80)
    varname_2 = models.CharField(max_length=80, blank=True, null=True)
    nl_name_2 = models.CharField(max_length=80, blank=True, null=True)
    type_2 = models.CharField(max_length=80)
    engtype_2 = models.CharField(max_length=80, blank=True, null=True)
    cc_2 = models.CharField(max_length=80, blank=True, null=True)
    hasc_2 = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    slug = AutoSlugField(populate_from='name_2')

    def __str__(self):
        return '{}, {}, {}'.format(
            self.name_2, self.name_1, self.name_0
        )

    @property
    def url(self):
        return reverse('country:division-detail', args=[self.slug])

    @property
    def json(self):
        return self.geom.json

    @property
    def geojson(self):
        data = json.loads(self.geom.geojson)
        content = '<a href="{}"><h4>{}</h4></a>'.format(
            self.url, str(self)
        )
        data['properties'] = {'popup_content': content}
        return data

    class Meta:
        ordering = ['name_2']



def create_travel_distances(new=False):
    # run to create travel details for the divisions
    if new:
        TravelDetails.objects.all().delete()
    for division_a in CountryDivision.objects.all():
        for division_b in CountryDivision.objects.all().annotate(
                _distance=Distance(Centroid('geom'),
                          Centroid(division_a.geom))):

            d = ureg.Quantity(division_b._distance.mi * ureg.mi)
            td = TravelDetails(distance=d, destination=division_a)

            td.save()
            division_b.distances.add(td)
            division_b.save()
            print(td)