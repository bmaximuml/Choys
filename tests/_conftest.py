# _conftest.py -- provides the actual configuration file for the tests that gets
# loaded in `test_plugin.py`
import pytest

from flask_sqlalchemy import SQLAlchemy
from os import environ

from HouseScrape.flaskr import create_app


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': environ['TEST_DATABASE_URL']
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


@pytest.fixture(scope='module')
def person(request, _db):
    '''
    Create a table to use for updating in the process of testing direct database access.
    '''
    class Person(_db.Model):
        __tablename__ = 'person'
        id = _db.Column(_db.Integer, primary_key=True)
        name = _db.Column(_db.String(80))

    # Create tables
    _db.create_all()

    @request.addfinalizer
    def drop_tables():
        _db.drop_all()

    return Person


@pytest.fixture(scope='module')
def account_address(request, _db, person):
    '''
    Create tables to use for testing deletes and relationships.
    '''
    class Account(_db.Model):
        __tablename__ = 'account'

        id = _db.Column(_db.Integer, primary_key=True)
        addresses = _db.relationship(
            'Address',
            back_populates='account',
        )

    class Address(_db.Model):
        __tablename__ = 'address'

        id = _db.Column(_db.Integer, primary_key=True)

        account_id = _db.Column(_db.Integer, _db.ForeignKey('account.id'))
        account = _db.relationship('Account', back_populates='addresses')

    # Create tables
    _db.create_all()

    @request.addfinalizer
    def drop_tables():
        _db.drop_all()

    return Account, Address
