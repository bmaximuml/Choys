import logging

from datetime import datetime
from flask import Blueprint, render_template, request
from math import ceil, floor

from . import get_location_data, get_location_data_alchemy

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    a = datetime.now()
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

    b = datetime.now()

    all_locations = get_location_data_alchemy()

    c = datetime.now()

    number_of_cards = 20
    page = int(request.args.get('page', default=1))

    sort = request.args.get('sort', default='score')
    sort_desc = request.args.get('dir', default='desc') == 'desc'

    d = datetime.now()

    for category in categories[1:]:
        loc_iter = [location._asdict()[category['id']] for location in all_locations]
        category['max'] = ceil(max(loc_iter))
        category['min'] = floor(min(loc_iter))

    e = datetime.now()

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

    f = datetime.now()

    for location in filtered_locations:
        all_locations.remove(location)

    g = datetime.now()

    sorted_locations = sorted(all_locations, key=lambda k: k._asdict()[sort], reverse=sort_desc)

    h = datetime.now()

    start = int((page - 1) * number_of_cards)
    end = start + 20
    logger.info(f'Total Locations: {len(all_locations)}')

    g = datetime.now()

    print('b: ' + str(b - a))
    print('c: ' + str(c - b))
    print('d: ' + str(d - c))
    print('e: ' + str(e - d))
    print('f: ' + str(f - e))
    print('g: ' + str(g - f))


    return render_template(
        'compare_locations.html',
        location_array=sorted_locations[start:end],
        year=datetime.now().year,
        sort=sort,
        sort_desc=sort_desc,
        categories=categories
    )
