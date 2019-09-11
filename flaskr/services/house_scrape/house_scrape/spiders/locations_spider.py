import logging
import re

from scrapy import Spider
from scrapy.exceptions import DropItem


def strip_commas(string):
    """Strips commas from a given string and returns a float rounded to 2dp"""
    if type(string) == bool:
        raise ValueError('String expected, received boolean')
    if len(str(string)) == 0:
        raise ValueError('Empty string supplied')
    just_commas = True
    for char in str(string):
        if char != ',':
            just_commas = False
    if just_commas:
        raise ValueError('String contained only commas')
    return round(float(re.sub(',', '', str(string))), 2)


def catch_and_zero(response, css, regex=None):
    """Return 0 if an IndexError is raised.

    This is used in some cases which may cause 'None's to be reported as '0's."""
    try:
        if regex is None:
            result = response.css(css).get()
        else:
            result = response.css(css).re(regex).pop(0)
        return result
    except IndexError:
        return '0'


class LocationsSpider(Spider):
    name = "locations"
    start_urls = [
            'https://www.home.co.uk/for_rent/current_rents_by_town.htm'
    ]

    def parse(self, response):
        logger = logging.getLogger()
        title = response.css('title::text').get()
        if 'Market Rents' in title:
            for li in response.css('li a::attr(href)').getall():
                yield response.follow(li, callback=self.parse)
        elif 'Market Rent Summary' in title:
            current_location = response.css('title::text').re(
                '(?!Home\\.co\\.uk:)[A-Za-z\\- ]*(?=Market Rent Summary)')[0].strip()
            logger.info(f'Crawling {current_location}')
            if current_location is not None and len(current_location) > 0:
                yield {
                    'name': current_location,
                    'total_properties': int(strip_commas(catch_and_zero(
                        response, 'div:nth-child(3) tr:nth-child(1) td:nth-child(2)::text'))),
                    'average_rent': strip_commas(catch_and_zero(
                        response, 'div:nth-child(3) tr:nth-child(3) td:nth-child(2)::text',
                        '(?!£)\\d{1,3}(?:[,\\.]\\d{3})*(?= pcm)')),
                    'rent_under_250': int(strip_commas(catch_and_zero(
                        response, 'div:nth-child(6) tr:nth-child(2) td:nth-child(2)::text'))),
                    'rent_250_to_500': int(strip_commas(catch_and_zero(
                        response, 'div:nth-child(6) tr:nth-child(3) td:nth-child(2)::text'))),
                }
            else:
                raise DropItem(f"Invalid name: '{current_location}'")
        elif 'Website Error' in title:
            raise DropItem(f"Website error detected. Page title: '{title}'")
        else:
            raise DropItem(f"Invalid page title: '{title}'")
