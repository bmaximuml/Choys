"""Tests for functions used to gather data"""

from HouseScrape.flaskr.services import run_house_scrape, run_google_maps_distance_matrix, calculate_scores, run_all_services
from HouseScrape.flaskr.model import Location
from HouseScrape.flaskr.exceptions import InvalidModeError, RequestError


def test_run_google_maps_distance_matrix(db_session):
    locations = db_session.query(Location).all()
    distance_matrix_counts = {}
    for loc in locations:
        distance_matrix_counts[loc.name] = len(loc.rental_data_rel)

    try:
        run_google_maps_distance_matrix(limit=20)
    except (InvalidModeError, RequestError) as e:
        assert (False,
                f'run_google_maps_distance_matrix threw an error: {str(e)}')

    new_locations = db_session.query(Location).all()

    for loc in new_locations:
        assert len(loc.rental_data_rel) in [distance_matrix_counts[loc.name],
                                            distance_matrix_counts[loc.name]
                                            + 1]
