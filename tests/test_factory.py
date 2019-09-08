from os import environ

from HouseScrape.flaskr import create_app


def test_config():
    assert not create_app({
        'SQLALCHEMY_DATABASE_URI': environ['TEST_DATABASE_URL']
    }).testing
    assert create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': environ['TEST_DATABASE_URL']
    }).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
