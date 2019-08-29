import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

# from db import get_db

bp = Blueprint('compare_locations', __name__)


@bp.route('/')
def index():
    # db = get_db()
    # data = db.execute(
    #     'SELECT id, name, total_properties, average_rent, rent_under_250, rent_250_to_500 '
    #     'FROM location ORDER by average_rent ASC'
    # ).fetchall()
    with open('/home/benji/Documents/HouseScrape/house_scrape/Location Files/locations.json') as f:
        j = json.loads(f.read())

    return render_template('compare_locations.html', json_locations=j)
