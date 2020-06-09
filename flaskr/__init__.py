import os

from flask import Flask
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    default_config = {
        'SECRET_KEY': os.environ['FLASK_SECRET_KEY'],
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    if test_config is None:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
            **default_config
        )
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=os.environ['TEST_DATABASE_URL'],
            **default_config
        )
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # a test page to confirm the google distance matrix functions work
    @app.route('/gmapi')
    def gmapi():
        from .services.g_maps import get_distance_matrix
        distance_duration = get_distance_matrix('Albrighton', 'London')
        result = (os.environ['GMAPI'] + str(distance_duration[0])
                                      + str(distance_duration[1])
                                      + str(int(distance_duration[0]))
                                      + str(int(distance_duration[1])))
        return result

    # a page to trigger a run of the google maps distance matrix api
    @app.route('/gm')
    def start_gmapi():
        from .services import run_google_maps_distance_matrix
        run_google_maps_distance_matrix()
        return 'Running...'

    from .model import db

    db.init_app(app=app)
    db.create_all(app=app)

    from . import compare_locations
    app.register_blueprint(compare_locations.bp)
    app.add_url_rule('/', endpoint='index')

    return app


def get_data_max(data, column):
    from logging import getLogger
    from sqlalchemy.sql.expression import func
    from .model import db

    logger = getLogger()
    try:
        result = float(db.session.query(func.max(column)).scalar())
        return result
    except NameError:
        logger.warning(f"Invalid data type or column name: {repr(column)}")
        return None


def test():
    return True


def get_location_data():
    from .model import db
    with open('flaskr/get_recent_data.sql') as sql_f:
        recent_data = db.engine.execute(sql_f.read())
    return recent_data.fetchall()


def get_location_data_alchemy():
    from sqlalchemy import desc
    from sqlalchemy.orm import aliased

    from .model import db, Location, RentalData, DistanceMatrixData, Scores

    aa = datetime.now()
    location0 = aliased(Location)
    rental_data0 = aliased(RentalData)
    distance_matrix_data0 = aliased(DistanceMatrixData)
    scores0 = aliased(Scores)

    rental_data1 = aliased(RentalData)
    distance_matrix_data1 = aliased(DistanceMatrixData)
    scores1 = aliased(Scores)

    ab = datetime.now()

    rental_data_datetime_stmt = db.session.query(
        rental_data1.datetime
    ).filter(
        rental_data1.location_name == rental_data0.location_name
    ).order_by(
        desc(rental_data1.datetime)
    ).limit(1).subquery()

    ac = datetime.now()

    distance_matrix_datetime_stmt = db.session.query(
        distance_matrix_data1.datetime
    ).filter(
        distance_matrix_data1.location_name == distance_matrix_data0.location_name
    ).order_by(
        desc(distance_matrix_data1.datetime)
    ).limit(1).subquery()

    ad = datetime.now()

    scores_datetime_stmt = db.session.query(
        scores1.datetime
    ).filter(
        scores1.location_name == scores0.location_name
    ).order_by(
        desc(scores1.datetime)
    ).limit(1).subquery()

    ae = datetime.now()

    recent_data = db.session.query(
        location0.name,
        rental_data0.total_properties,
        rental_data0.average_rent,
        rental_data0.rent_under_250,
        rental_data0.rent_250_to_500,
        distance_matrix_data0.distance_to_london_text,
        distance_matrix_data0.distance_to_london,
        distance_matrix_data0.duration_to_london_text,
        distance_matrix_data0.duration_to_london,
        scores0.score
    ).filter(
        rental_data0.location_name == location0.name
    ).filter(
        distance_matrix_data0.location_name == location0.name
    ).filter(
        scores0.location_name == location0.name
    ).group_by(
        rental_data0.location_name,
        rental_data0.total_properties,
        rental_data0.average_rent,
        rental_data0.rent_under_250,
        rental_data0.rent_under_250,
        rental_data0.datetime,
        distance_matrix_data0.location_name,
        distance_matrix_data0.distance_to_london_text,
        distance_matrix_data0.distance_to_london,
        distance_matrix_data0.duration_to_london_text,
        distance_matrix_data0.duration_to_london,
        distance_matrix_data0.datetime,
        scores0.location_name,
        scores0.score,
        scores0.datetime,
        location0.name
    ).having(
        rental_data0.datetime == rental_data_datetime_stmt
    ).having(
        distance_matrix_data0.datetime == distance_matrix_datetime_stmt
    ).having(
        scores0.datetime == scores_datetime_stmt
    )

    af = datetime.now()

    result = recent_data

    print('ab: ' + str(ab - aa))
    print('ac: ' + str(ac - ab))
    print('ad: ' + str(ad - ac))
    print('ae: ' + str(ae - ad))
    print('af: ' + str(af - ae))
    print('ag: ' + str(ag - af))

    return result
