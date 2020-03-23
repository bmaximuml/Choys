import logging

from datetime import datetime
from flask import Blueprint, render_template, request

from . import get_location_data

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    logger = logging.getLogger()

    all_locations = get_location_data()

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
