import pytest
from tickets.app import app, db
from tickets.models import Event, Purchase
from tickets.views import *  # NOQA


@pytest.fixture
def client():
    with app.app_context():
        yield app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_charge_no_data(client):
    response = client.post('charge')
    assert response.status_code == 400


def test_charge_no_event(client):
    form_data = {
        'stripeEmail': 'ty@gmail.com',
        'stripeToken': 'deadbeef',
        'ticket_count': 2,
        'event_id': 42000
    }
    response = client.post('charge', data=form_data, content_type='multipart/form-data')
    assert response.status_code == 404


def test_charge_no_purchase_on_failed_stripe(client):
    # Test that no purchase is saved in database when charge via Stripe fails.

    # Given a new event and a proper request
    with db.db_engine.execution_context():
        event = Event.create(price=2500, title='METZ', description='at Logo')
    form_data = {
        'stripeEmail': 'ty@gmail.com',
        'stripeToken': 'deadbeef',
        'ticket_count': 2,
        'event_id': event.id
    }

    # When we request a charge
    response = client.post('charge', data=form_data, content_type='multipart/form-data')

    # Then the event has no purchases, ie no charge was recorded.
    with pytest.raises(Purchase.DoesNotExist):
        Purchase.select().where(Purchase.event_id == event.id).get()
    assert response.status_code == 500


def test_charge_successful(client):
    def mock_charge(self, token):
        pass

    Purchase.charge = mock_charge

    # Given a new event and a proper request
    with db.db_engine.execution_context():
        event = Event.create(price=2500, title='METZ', description='at Logo')
    form_data = {
        'stripeEmail': 'ty@gmail.com',
        'stripeToken': 'deadbeef',
        'ticket_count': 2,
        'event_id': event.id
    }

    # When we request a charge
    response = client.post('charge', data=form_data, content_type='multipart/form-data')

    # Then a purchase with tickets is created.
    purchase = Purchase.select().where(Purchase.event_id == event.id).get()
    assert purchase.email == 'ty@gmail.com'
    assert len(purchase.tickets) == 2

    # And a redirect is returned.
    assert response.status_code == 302


def test_purchase_found(client):
    with db.db_engine.execution_context():
        event = Event.create(price=2500, title='METZ', description='at Logo')
        p = event.create_purchase(email='karsten@ticketfarm.de')

    response = client.get('purchase/{}?secret={}'.format(p.id, p.secret))
    assert response.status_code == 200


def test_purchase_not_found(client):
    response = client.get('purchase/42')
    assert response.status_code == 404


def test_ticket_found(client):
    with db.db_engine.execution_context():
        event = Event.create(price=2500, title='METZ', description='at Logo')
        purchase = Purchase.create(email='karsten@ticketfarm.de', event=event)
        ticket = purchase.create_tickets(1)[0]
        ticket.secret = '922415d39433cdc6a258bddb1062f808cdbd1595a8132e443ec85b65f6c8edb2'
        ticket.save()

    # Query ticket.
    response = client.get('ticket/{}?secret={}'.format(ticket.id, ticket.secret))
    assert response.status_code == 200

    # Query ticket QR code as svg.
    response = client.get('ticket/{}.svg?secret={}'.format(ticket.id, ticket.secret))
    assert response.status_code == 200

    # All data was streamed.
    assert response.calculate_content_length() == 3409


def test_ticket_not_found(client):
    response = client.get('ticket/42')
    assert response.status_code == 404

    response = client.get('ticket/42.svg?secret=deadbeef')
    assert response.status_code == 404
