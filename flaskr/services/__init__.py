"""Functions to fetch external data to be used in the application"""

from datetime import datetime
from logging import getLogger
from os import environ
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .. import get_data_max, get_location_data
from ..model import db, Location, RentalData, DistanceMatrixData, Scores
from ..exceptions import NoResultsError
from .uk_locations_scrape.uk_locations_scrape.spiders.locations_spider import LocationsSpider
from .g_maps import get_distance_matrix


def run_uk_locations_scrape():
    """Run the scrapy spider to fetch rental data from home.co.uk"""
    environ['SCRAPY_SETTINGS_MODULE'] = ('Choys.flaskr.services.'
                                         'uk_locations_scrape.uk_locations_scrape.settings')
    settings = get_project_settings()
    settings['LOG_LEVEL'] = 'INFO'
    process = CrawlerProcess(settings=settings)
    process.crawl('locations')
    process.start()
    print('Finished crawling')


def run_google_maps_distance_matrix(limit=None):
    """Calculate and store distance information for each existing location.

    Uses Google Maps Distance Matrix API"""
    logger = getLogger()
    if limit is None:
        all_locations = Location.query.all()
    else:
        all_locations = Location.query.limit(limit).all()
    for location in all_locations:
        try:
            distance_duration = get_distance_matrix(location.name, 'London')
        except NoResultsError:
            distance_duration = None
        if distance_duration is not None:
            db.session.add(DistanceMatrixData(
                distance_to_london=distance_duration[1]['value'],
                distance_to_london_text=distance_duration[1]['text'],
                duration_to_london=distance_duration[0]['value'],
                duration_to_london_text=distance_duration[0]['text'],
                datetime=datetime.utcnow(),
                location_name=location.name

            ))
            logger.info(f'Added distance matrix information for '
                        f'{location.name}')
        else:
            logger.warning(f'Could not add distance matrix information for '
                           f'{location.name}')
    db.session.commit()


def score_component(component, power, multiplier):
    if component is not None and component != 0:
        return (float(component) ** power) * multiplier
    else:
        return 0


def calculate_scores():
    """Calculate an updated score for each existing Location"""
    all_locations = get_location_data()
    logger = getLogger()

    for loc in all_locations:
        logger.info(f'Calculating score for {loc.name}...')
        score = 0
        components = [
            [loc.total_properties, 0.17, 1.7],
            [loc.average_rent, -0.37, 150.0],
            [loc.duration_to_london, -0.24, 40.0]
        ]
        for component in components:
            score += score_component(*component)

        db.session.add(Scores(
            score=score,
            datetime=datetime.utcnow(),
            location_name=loc.name,
        ))
        logger.info(f'Added score for {loc.name}.')
    db.session.commit()
    logger.warning('Calculated scores.')


def run_all_services():
    """Fetch data from all available sources"""
    run_uk_locations_scrape()
    run_google_maps_distance_matrix()
    calculate_scores()
