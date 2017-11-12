import pytest
from tickets.app import app
from tickets.views import *  # NOQA


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_purchase_not_found(client):
    response = client.get('purchase/42')
    assert response.status_code == 404


def test_ticket_not_found(client):
    response = client.get('ticket/42')
    assert response.status_code == 404
