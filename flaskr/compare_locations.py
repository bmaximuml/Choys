import logging

from datetime import datetime
from flask import Blueprint, render_template

from .model import db

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    logger = logging.getLogger()

    with open('flaskr/services/get_recent_data.sql') as sql_f:
        recent_data = db.engine.execute(sql_f.read())

    all_locations = recent_data.fetchall()

    logger.info(f'Total Locations: {len(all_locations)}')
    return render_template(
        'compare_locations.html',
        location_array=all_locations,
        year=datetime.now().year
    )
