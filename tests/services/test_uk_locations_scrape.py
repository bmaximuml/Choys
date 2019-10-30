"""Tests for Scrapy and its spiders"""

import pytest

from scrapy.http import HtmlResponse

from . import location_list
from Choys.flaskr.services.uk_locations_scrape.uk_locations_scrape.spiders.\
      locations_spider import strip_commas, catch_and_zero


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('3,000', 3000.00),
        ("200", 200.00),
        ("28439324", 28439324.00),
        ("2,2,,3,4,5,,6", 223456.00),
        ("20,456,879", 20456879.00),
        (4586, 4586.00),
        (3, 3.00),
        (-4, -4.00),
        (-6789, -6789.00),
        ('-678', -678.00),
        ('-12,433,726', -12433726.00),
        (4586.0, 4586.00),
        (3.0, 3.00),
        (-4.0, -4.00),
        (-6789.0, -6789.00),
        ('-678.0', -678.00),
        (4586.25, 4586.25),
        (3.56, 3.56),
        (-4.2165, -4.22),
        (-4.215, -4.21),
        (-4.2145, -4.21),
        (-6789.56, -6789.56),
        ('-678.1', -678.10),
    ]
)
def test_strip_commas_valid(test_input, expected):
    """Test the strip_commas function with valid inputs"""
    assert strip_commas(test_input) == expected


@pytest.mark.parametrize(
    "test_input",
    [
        'x',
        'fish',
        'b1',
        'True',
        True,
        False,
        'iqweuoiqwn',
        '87h23n89',
        ',',
        ',,,,,,',
        ',,frg,,',
        ';#[];',
        '`',
        '\\',
        '\\\\'
    ]
)
def test_strip_commas_invalid(test_input):
    """Test the strip_commas function with invalid inputs"""
    with pytest.raises(ValueError):
        strip_commas(test_input)


@pytest.mark.parametrize(
    'test_file,expected',
    list(zip(
        location_list,
        [
            '2',
            '60',
            '74',
            '8',
            '9',
            '1',
            '44',
            '2',
            '283',
            '24',
            '8',
            '5',
            '164',
            '3',
            '17',
            '4',
            '4',
            '1,672',
            '6',
            '141',
            '140',
            '50',
            '2,150',
            '489',
            '39',
            '613',
            '60',
            '130',
            '21',
            '39',
            '75',
            '20',
            '23',
            '27',
            '6',
            '211',
            '4',
            '4',
            '10',
            '6',
            '18',
            '2',
            '55',
            '23',
            '7',
            '16',
            '9',
            '46',
            '27',
            '10',
            '70',
            '19',
        ]
    ))
)
def test_catch_and_zero_total_properties(test_file, expected):
    """Test the catch_and_zero function with using total_properties data"""
    with open(f'tests/services/html/{test_file}') as f:
        html = f.read()
        result = catch_and_zero(
            HtmlResponse('https://home.co.uk/', body=html, encoding='utf-8'),
            'div:nth-child(3) tr:nth-child(1) td:nth-child(2)::text'
        )
        assert result == expected


@pytest.mark.parametrize(
    'test_file,expected',
    list(zip(
        location_list,
        [
            '1,925',
            '1,109',
            '710',
            '842',
            '1,433',
            '2,500',
            '2,004',
            '799',
            '909',
            '1,017',
            '1,069',
            '1,200',
            '1,148',
            '1,300',
            '1,285',
            '3,895',
            '1,924',
            '2,075',
            '1,012',
            '848',
            '1,141',
            '1,089',
            '1,384',
            '863',
            '900',
            '1,303',
            '6,630',
            '1,990',
            '735',
            '1,896',
            '923',
            '1,006',
            '1,038',
            '583',
            '1,584',
            '959',
            '1,080',
            '1,637',
            '1,178',
            '1,881',
            '991',
            '1,013',
            '1,270',
            '1,440',
            '822',
            '874',
            '1,356',
            '890',
            '939',
            '1,388',
            '887',
            '1,282',
        ]
    ))
)
def test_catch_and_zero_average_rent(test_file, expected):
    """Test the catch_and_zero function with using average_rent data"""
    with open(f'tests/services/html/{test_file}') as f:
        html = f.read()
        result = catch_and_zero(
            HtmlResponse('https://home.co.uk/', body=html, encoding='utf-8'),
            'div:nth-child(3) tr:nth-child(3) td:nth-child(2)::text',
            '(?!£)\\d{1,3}(?:[,\\.]\\d{3})*(?= pcm)'
        )
        assert result == expected


@pytest.mark.parametrize(
    'test_file,expected',
    list(zip(
        location_list,
        [
            '0',
            '3',
            '1',
            '0',
            '0',
            '0',
            '0',
            '0',
            '4',
            '0',
            '0',
            '0',
            '1',
            '0',
            '0',
            '0',
            '0',
            '1',
            '0',
            '1',
            '0',
            '0',
            '7',
            '2',
            '0',
            '3',
            '0',
            '0',
            '0',
            '0',
            '0',
            '1',
            '0',
            '1',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
        ]
    ))
)
def test_catch_and_zero_rent_under_250(test_file, expected):
    """Test the catch_and_zero function with using rent_under_250 data"""
    with open(f'tests/services/html/{test_file}') as f:
        html = f.read()
        result = catch_and_zero(
            HtmlResponse('https://home.co.uk/', body=html, encoding='utf-8'),
            'div:nth-child(6) tr:nth-child(2) td:nth-child(2)::text'
        )
        assert result == expected


@pytest.mark.parametrize(
    'test_file,expected',
    list(zip(
        location_list,
        [
            '0',
            '0',
            '11',
            '0',
            '0',
            '0',
            '0',
            '0',
            '22',
            '1',
            '0',
            '0',
            '8',
            '0',
            '1',
            '0',
            '0',
            '4',
            '0',
            '20',
            '9',
            '1',
            '49',
            '78',
            '6',
            '13',
            '0',
            '0',
            '1',
            '0',
            '2',
            '0',
            '1',
            '10',
            '0',
            '16',
            '0',
            '0',
            '0',
            '0',
            '1',
            '0',
            '1',
            '0',
            '1',
            '1',
            '0',
            '0',
            '0',
            '0',
            '0',
            '3',
        ]
    ))
)
def test_catch_and_zero_rent_250_to_500(test_file, expected):
    """Test the catch_and_zero function with using rent_250_to_500 data"""
    with open(f'tests/services/html/{test_file}') as f:
        html = f.read()
        result = catch_and_zero(
            HtmlResponse('https://home.co.uk/', body=html, encoding='utf-8'),
            'div:nth-child(6) tr:nth-child(3) td:nth-child(2)::text'
        )
        assert result == expected
