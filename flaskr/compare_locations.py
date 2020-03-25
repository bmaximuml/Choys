import logging

from datetime import datetime
from flask import Blueprint, render_template, request
from math import ceil, floor

from . import get_location_data

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    categories = [
        {'id': 'name', 'title': 'Location'},
        {'id': 'total_properties', 'title': 'Number of Properties'},
        {'id': 'average_rent', 'title': 'Average Rent (£ / pcm)'},
        {'id': 'rent_under_250', 'title': 'Number of properties under £250 pcm'},
        {'id': 'rent_250_to_500', 'title': 'Number of properties between £250 and £500 pcm'},
        {'id': 'distance_to_london', 'title': 'Distance to London'},
        {'id': 'duration_to_london', 'title': 'Duration to London'},
        {'id': 'score', 'title': 'Score'}
    ]

    logger = logging.getLogger()

    all_locations = get_location_data()

    sort = request.args.get('sort', default='score')
    sort_desc = request.args.get('dir', default='desc') == 'desc'

    for category in categories[1:]:
        category['max'] = ceil(max([location[category['id']] for location in all_locations]))
        category['min'] = floor(min([location[category['id']] for location in all_locations]))

    filtered_locations = []
    for i, location in enumerate(all_locations):
        for category in categories:
            if request.args.get(category['id']) is None:
                # No value set for category, skip to next category
                continue

            category_switch = request.args.get(f"{category['id']}_switch", default='or-less')

            try:
                location_category = float(location[category['id']])
                request_category = float(request.args.get(category['id']))
            except ValueError:
                location_category = str(location[category['id']])
                request_category = str(request.args.get(category['id']))

            if ((
                    category_switch == 'or-more' and
                    location_category < request_category
                ) or (
                    category_switch == 'or-less' and
                    location_category > request_category
            )):
                filtered_locations.append(location)
                # If location is removed, don't check remaining categories
                break

    for location in filtered_locations:
        all_locations.remove(location)

    logger.info(f'Total Locations: {len(all_locations)}')
    return render_template(
        'compare_locations.html',
        location_array=all_locations,
        year=datetime.now().year,
        sort=sort,
        sort_desc=sort_desc,
        categories=categories
    )
