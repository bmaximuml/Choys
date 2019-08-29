from flask import (
    Blueprint, render_template
)

from flaskr.model import Locations

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    location_list = []
    all_orm_locations = Locations.query.filter_by(newest=True)
    for location in all_orm_locations:
        location_list.append(Location(
            location.location_name,
            location.total_properties,
            location.average_rent,
            location.rent_250_to_500,
            location.rent_250_to_500
        ))

    return render_template('compare_locations.html', location_array=location_list)


class Location:
    def __init__(self, location_name, total_properties=0, average_rent=None, rent_under_250=0, rent_250_to_500=0):
        self.location_name = location_name
        self.total_properties = total_properties
        self.average_rent = average_rent
        self.rent_under_250 = rent_under_250
        self.rent_250_to_500 = rent_250_to_500

    def __str__(self):
        return str(self.location_name)

    def __iter__(self):
        self.n = 'location_name'
        return self

    def __next__(self):
        if self.n is not None:
            if self.n == 'location_name':
                self.n = 'total_properties'
                return self.location_name
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
                self.n = None
                return self.rent_250_to_500
            else:
                raise AttributeError('Invalid attribute.')
        else:
            raise StopIteration
