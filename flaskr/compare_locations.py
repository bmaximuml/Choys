import logging

from flask import Blueprint, render_template

from . import get_data_for_location_name
from .model import db, Location, RentalData, DistanceMatrixData, Scores

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    logger = logging.getLogger()
    location_list = []
    all_locations = db.session.query(Location).all()

    for loc in all_locations:
        rental_data = get_data_for_location_name(RentalData, loc.name)
        distance_matrix_data = get_data_for_location_name(DistanceMatrixData,
                                                          loc.name)
        scores = get_data_for_location_name(Scores, loc.name)

        distance_to_london_text = distance_matrix_data.distance_to_london_text
        duration_to_london_text = distance_matrix_data.duration_to_london_text

        if distance_matrix_data is not None and rental_data is not None:
            location_list.append(Row(
                name=loc.name,
                total_properties=(rental_data.total_properties
                                  if rental_data is not None else None),
                average_rent=(rental_data.average_rent
                              if rental_data is not None else None),
                rent_under_250=(rental_data.rent_under_250
                                if rental_data is not None else None),
                rent_250_to_500=(rental_data.rent_250_to_500
                                 if rental_data is not None else None),
                distance_to_london=(distance_matrix_data.distance_to_london
                                    if distance_matrix_data is not None
                                    else None),
                duration_to_london=(distance_matrix_data.duration_to_london
                                    if distance_matrix_data is not None
                                    else None),
                distance_to_london_text=(distance_to_london_text
                                         if distance_matrix_data is not None
                                         else None),
                duration_to_london_text=(duration_to_london_text
                                         if distance_matrix_data is not None
                                         else None),
                score=(scores.score if scores is not None else None)
            ))

    logger.info(f'Total Locations: {len(all_locations)}')
    return render_template('compare_locations.html', location_array=location_list, year=date.today().year)


class Row:
    def __init__(self,
                 name,
                 total_properties=0,
                 average_rent=None,
                 rent_under_250=0,
                 rent_250_to_500=0,
                 distance_to_london=None,
                 duration_to_london=None,
                 distance_to_london_text=None,
                 duration_to_london_text=None,
                 score=None
                 ):
        self.name = name
        self.total_properties = total_properties
        self.average_rent = average_rent
        self.rent_under_250 = rent_under_250
        self.rent_250_to_500 = rent_250_to_500
        self.distance_to_london = [distance_to_london, distance_to_london_text]
        self.duration_to_london = [duration_to_london, duration_to_london_text]
        self.score = score

    def __str__(self):
        return str(self.name)

    def __iter__(self):
        self.n = 'name'
        return self

    def __next__(self):
        if self.n is not None:
            if self.n == 'name':
                self.n = 'total_properties'
                return self.name
            elif self.n == 'total_properties':
                self.n = 'average_rent'
                return self.total_properties
            elif self.n == 'average_rent':
                self.n = 'rent_under_250'
                return self.average_rent
            elif self.n == 'rent_under_250':
                self.n = 'rent_250_to_500'
                return self.rent_under_250
            elif self.n == 'rent_250_to_500':
                self.n = 'distance_to_london'
                return self.rent_250_to_500
            elif self.n == 'distance_to_london':
                self.n = 'duration_to_london'
                return self.distance_to_london
            elif self.n == 'duration_to_london':
                self.n = 'score'
                return self.duration_to_london
            elif self.n == 'score':
                self.n = None
                return self.score
            else:
                raise AttributeError('Invalid attribute.')
        else:
            raise StopIteration
