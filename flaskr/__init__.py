import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
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


def get_data_for_location_name(data, location_name):
    from logging import getLogger
    from sqlalchemy import desc
    from .model import db  # , RentalData, DistanceMatrixData, Scores

    logger = getLogger()
    try:
        result = db.session.query(data).filter(
            location_name == data.location_name
        ).order_by(desc(data.datetime)).first()
        return result
    except NameError:
        logger.warning(f'Invalid data type: {repr(data)}')
        return None


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

