import os
import pytest

# This import prevents SQLAlchemy from throwing an AttributeError
# claiming that <class 'object'> is already a registered type -- it is suspicious
# code and should eventually be either confirmed to fix a bug, or removed
from flask_sqlalchemy import SQLAlchemy

from HouseScrape.flaskr import create_app

pytest_plugins = ['pytester']


@pytest.fixture
def db_testdir(conftest, testdir):
    '''
    Set up a temporary test directory loaded with the configuration file for
    the tests.
    '''
    testdir.makeconftest(conftest)

    return testdir


@pytest.fixture(scope='module')
def conftest():
    '''
    Load configuration file for the tests to a string, in order to run it in
    its own temporary directory.
    '''
    with open(os.path.join('tests', '_conftest.py'), 'r') as conf:
        conftest = conf.read()

    return conftest


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ['TEST_DATABASE_URL']
    }

    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def _db(app, request):
    """Session-wide test database."""
    def teardown():
        db.drop_all()

    db = SQLAlchemy(app=app)

    request.addfinalizer(teardown)
    return db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
