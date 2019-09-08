from datetime import datetime
from os import environ
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from logging import getLogger

from .. import get_data_for_location_name, get_data_max
from ..model import db, Location, RentalData, DistanceMatrixData, Scores
from .house_scrape.house_scrape.spiders.locations_spider import LocationsSpider
from .g_maps import get_distance_matrix


def run_house_scrape():
    # environ.setdefault('SCRAPY_SETTINGS_MODULE', 'HouseScrape.flaskr.services.house_scrape.house_scrape.settings')
    environ['SCRAPY_SETTINGS_MODULE'] = 'HouseScrape.flaskr.services.house_scrape.house_scrape.settings'
    settings = get_project_settings()
    settings['LOG_LEVEL'] = 'INFO'
    process = CrawlerProcess(settings=settings)
    process.crawl('locations')
    # process.crawl(LocationsSpider)
    process.start()
    print('Finished crawling')


def run_google_maps_distance_matrix(limit=None):
    logger = getLogger()
    if limit is None:
        all_locations = Location.query.all()
    else:
        all_locations = Location.query.limit(limit).all()
    for location in all_locations:
        distance_duration = get_distance_matrix(location.name, 'London')
        if distance_duration[0] is not None and distance_duration[1] is not None:
            db.session.add(DistanceMatrixData(
                distance_to_london=distance_duration[1]['value'],
                distance_to_london_text=distance_duration[1]['text'],
                duration_to_london=distance_duration[0]['value'],
                duration_to_london_text=distance_duration[0]['text'],
                datetime=datetime.utcnow(),
                location_name=location.name

            ))
            logger.info(f'Added distance matrix information for {location.name}')
        else:
            logger.warning(f'Could not add distance matrix information for {location.name}')
    db.session.commit()


def calculate_scores():
    all_locations = db.session.query(Location).all()
    logger = getLogger()

    # modifiers = {}
    # db_modifiers = db.session.query(Modifiers).all()
    # for mod in db_modifiers:
    #     modifiers[mod.property] = int(mod.modifier)
    modifiers = {'total_properties': 0.0,
                 'average_rent': float(1000.0),
                 'rent_under_250': 0.0,
                 'rent_250_to_500': 0.0,
                 'distance_to_london': 0.0,
                 'duration_to_london': float(30)
                 }
    for loc in all_locations:
        logger.info(f'Calculating score for {loc.name}...')
        rental_data = get_data_for_location_name(RentalData, loc.name)
        distance_matrix_data = get_data_for_location_name(DistanceMatrixData, loc.name)
        if rental_data is not None and distance_matrix_data is not None:
            max_total_properties = float(get_data_max(RentalData, RentalData.total_properties))
            max_average_rent = float(get_data_max(RentalData, RentalData.average_rent))
            max_rent_under_250 = float(get_data_max(RentalData, RentalData.rent_under_250))
            max_rent_250_to_500 = float(get_data_max(RentalData, RentalData.rent_250_to_500))
            max_distance_to_london = float(get_data_max(DistanceMatrixData, DistanceMatrixData.distance_to_london))
            max_duration_to_london = float(get_data_max(DistanceMatrixData, DistanceMatrixData.duration_to_london))
            # score = ((modifiers['total_properties'] * float(rental_data.total_properties)) / max_total_properties) + \
            #         ((modifiers['average_rent'] * max_average_rent ** 0.5) / float(rental_data.average_rent) ** 0.5) + \
            #         ((modifiers['rent_under_250'] * float(rental_data.rent_under_250)) / max_rent_under_250) + \
            #         ((modifiers['rent_250_to_500'] * float(rental_data.rent_250_to_500)) / max_rent_250_to_500) + \
            #         ((modifiers['distance_to_london'] * max_distance_to_london) / float(distance_matrix_data.distance_to_london)) + \
            #         ((modifiers['duration_to_london'] * max_duration_to_london) / float(distance_matrix_data.duration_to_london))
            # score = (1.0 + (modifiers['total_properties'] * float(rental_data.total_properties)) / max_total_properties) * \
            #         (1.0 + (modifiers['average_rent'] / float(rental_data.average_rent))) * \
            #         (1.0 + (modifiers['rent_under_250'] * float(rental_data.rent_under_250)) / max_rent_under_250) * \
            #         (1.0 + (modifiers['rent_250_to_500'] * float(rental_data.rent_250_to_500)) / max_rent_250_to_500) * \
            #         (1.0 + (modifiers['distance_to_london'] * max_distance_to_london) / float(distance_matrix_data.distance_to_london)) * \
            #         (1.0 + (modifiers['duration_to_london'] / float(distance_matrix_data.duration_to_london)))
            # score = (1.0 + (modifiers['average_rent'] / ((float(rental_data.average_rent) ** 2) / max_average_rent))) * \
            #         (1.0 + (modifiers['duration_to_london'] / ((float(distance_matrix_data.duration_to_london) ** 0.5) / max_duration_to_london)))
            # score = (1.0 + (1.0 / (float(rental_data.average_rent)))) * (1.0 + (1.0 / (float(distance_matrix_data.duration_to_london))))

            total_properties_score = (float(rental_data.total_properties) ** 0.17) * 1.7
            average_rent_score = (float(rental_data.average_rent) ** -0.37) * 150.0
            duration_to_london_score = (float(distance_matrix_data.duration_to_london) ** -0.24) * 40.0
            score = average_rent_score + duration_to_london_score + total_properties_score
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
    run_house_scrape()
    run_google_maps_distance_matrix()
    calculate_scores()
