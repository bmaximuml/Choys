import pytest

from . import location_list
from HouseScrape.flaskr.services.g_maps import (get_duration, get_distance,
                                                get_distance_matrix)


@pytest.mark.parametrize('start', location_list[:30])
@pytest.mark.parametrize('dest', ['London'])
@pytest.mark.parametrize('mode', ['driving', 'transit', 'bicycling', 'walking'])
@pytest.mark.parametrize('language', ['en-GB'])
@pytest.mark.parametrize('region', ['uk'])
@pytest.mark.parametrize('units', ['metric', 'imperial'])
def test_get_distance_matrix_valid(start, dest, mode, language, region, units):
    result = get_distance_matrix(start, dest, mode, language, region, units)

    assert len(result) == 2
    assert len(result[0]) == 2
    assert len(result[1]) == 2

    assert 'text' in result[0]
    assert 'value' in result[0]
    assert 'text' in result[1]
    assert 'value' in result[1]

    assert type(result[0]['text']) == str
    assert type(result[0]['value']) == int
    assert type(result[1]['text']) == str
    assert type(result[1]['value']) == int
