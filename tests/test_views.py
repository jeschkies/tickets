import pytest
from tickets.app import app
from tickets.views import *  # NOQA


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_charge_no_data(client):
    response = client.post('charge')
    assert response.status_code == 400


def test_purchase_found(client):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    p = event.create_purchase(email='karsten@ticketfarm.de')

    response = client.get('purchase/{}?secret={}'.format(p.id, p.secret))
    assert response.status_code == 200


def test_purchase_not_found(client):
    response = client.get('purchase/42')
    assert response.status_code == 404


def test_ticket_found(client):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    purchase = Purchase.create(email='karsten@ticketfarm.de', event=event)
    ticket = purchase.create_tickets(1)[0]

    response = client.get('ticket/{}?secret={}'.format(ticket.id, ticket.secret))
    assert response.status_code == 200

def test_ticket_not_found(client):
    response = client.get('ticket/42')
    assert response.status_code == 404
