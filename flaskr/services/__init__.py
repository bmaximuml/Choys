"""Functions to fetch external data to be used in the application"""

from datetime import datetime
from logging import getLogger
from os import environ
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .. import get_data_for_location_name, get_data_max
from ..model import db, Location, RentalData, DistanceMatrixData, Scores
from ..exceptions import NoResultsError
from .uk_locations_scrape.uk_locations_scrape.spiders.locations_spider import LocationsSpider
from .g_maps import get_distance_matrix


def get_location_data():
    with open('flaskr/services/get_recent_data.sql') as sql_f:
        recent_data = db.engine.execute(sql_f.read())
    return recent_data.fetchall()


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


def calculate_scores():
    """Calculate an updated score for each existing Location"""
    all_locations = db.session.query(Location).all()
    logger = getLogger()

    for loc in all_locations:
        logger.info(f'Calculating score for {loc.name}...')
        rental_data = get_data_for_location_name(RentalData, loc.name)
        distance_matrix_data = get_data_for_location_name(
            DistanceMatrixData,
            loc.name
        )
        if rental_data is not None and distance_matrix_data is not None:
            total_properties_score = (
                (
                    float(rental_data.total_properties)
                    ** 0.17
                ) * 1.7
            )
            average_rent_score = (
                (
                    float(rental_data.average_rent)
                    ** -0.37
                ) * 150.0
            )
            duration_to_london_score = (
                (
                    float(distance_matrix_data.duration_to_london)
                    ** -0.24
                ) * 40.0
            )
            score = (
                average_rent_score
                + duration_to_london_score
                + total_properties_score
            )
            db.session.add(Scores(
                score=score,
                datetime=datetime.utcnow(),
                location_name=loc.name,
            ))
            logger.info(f'Added score for {loc.name}.')
        else:
            logger.warning(f'Could not calculate score for {loc.name}')
    db.session.commit()
    logger.warning('Calculated scores.')


def run_all_services():
    """Fetch data from all available sources"""
    run_uk_locations_scrape()
    run_google_maps_distance_matrix()
    calculate_scores()
