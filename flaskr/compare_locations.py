import logging

from datetime import datetime
from flask import Blueprint, render_template, request

from . import get_location_data

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    categories = [
        'name',
        'total_properties',
        'average_rent',
        'rent_under_250',
        'rent_250_to_500',
        'distance_to_london',
        'duration_to_london',
        'score'
    ]

    logger = logging.getLogger()

    all_locations = get_location_data()

    for location in all_locations:
        for category in categories:
            if request.args.get(category) is None:
                # No value set for category, skip to next category
                continue

            category_switch = request.args.get(f'{category}_switch', default='or-less')

            try:
                location_category = float(location[category])
                request_category = float(request.args.get(category))
            except ValueError:
                location_category = str(location[category])
                request_category = str(request.args.get(category))

            if ((
                    category_switch == 'or-more' and
                    location_category < request_category
                ) or (
                    category_switch == 'or-less' and
                    location_category > request_category
            )):
                all_locations.remove(location)
                # If location is removed, don't check remaining categories
                break

    sort = request.args.get('sort', default='name')
    sort_desc = request.args.get('dir', default='asc') == 'desc'

    logger.info(f'Total Locations: {len(all_locations)}')
    return render_template(
        'compare_locations.html',
        location_array=all_locations,
        year=datetime.now().year,
        sort=sort,
        sort_desc=sort_desc
    )
