import os
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder, CountryDivision
from django.contrib.gis.gdal import DataSource

world_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'nl_name_1': 'NL_NAME_1',
    'gid_2': 'GID_2',
    'name_2': 'NAME_2',
    'varname_2': 'VARNAME_2',
    'nl_name_2': 'NL_NAME_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'cc_2': 'CC_2',
    'hasc_2': 'HASC_2',
    'geom': 'MULTIPOLYGON',
}

world_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'gadm36_GBR_2.shp'),
)
ds = DataSource(world_shp)
lyr = ds[0]


def run(verbose=True):
    # import the data, we have remove the FIPS mapping because it caused a problem during the import
    lm = LayerMapping(CountryDivision, world_shp, world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

run(verbose=False)
