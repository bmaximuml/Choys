from datetime import datetime
from logging import getLogger

from ..model import db, Location, DistanceMatrixData
from .house_scrape.house_scrape.spiders.locations_spider import LocationsSpider
from .g_maps import get_distance_matrix


def run_google_maps_distance_matrix():
    logger = getLogger()
    all_locations = Location.query.all()
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
