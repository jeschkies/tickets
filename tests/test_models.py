import pytest
from tickets.app import db
from tickets.models import Event, Purchase, Ticket


@pytest.fixture
def database():
    db.db_engine.connect()
    yield db
    db.db_engine.close()
    # TODO: Clean all create events afterwards


def test_event(database):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    fetched_event = Event.select().where(Event.id == event.id).get()

    assert fetched_event.price == 2500
    assert fetched_event.title == 'METZ'
    assert fetched_event.description == 'at Logo'


def test_purchase(database):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    purchase_1 = Purchase.create(email='karsten@ticketfarm.de', event=event)
    purchase_2 = event.create_purchase(email='karsten@ticketfarm.de')

    assert purchase_1.secret != purchase_2.secret

    fetched_purchase_1 = Purchase.select().where(
        Purchase.id == purchase_1.id).get()

    assert fetched_purchase_1.email == 'karsten@ticketfarm.de'

    ids = sorted([p.id for p in event.purchases])
    assert ids == sorted([purchase_1.id, purchase_2.id])


def test_purchase_of(database):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    purchase = event.create_purchase(email='karsten@ticketfarm.de')

    selected = Purchase.of(purchase.id, purchase.secret)
    selected.email == 'karsten@ticketfarm.de'

    with pytest.raises(Purchase.DoesNotExist):
        Purchase.of(42, 'notasecret')


def test_ticket(database):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    purchase = Purchase.create(email='karsten@ticketfarm.de', event=event)
    tickets = purchase.create_tickets(2)
    ticket_ids = sorted([t.id for t in tickets])

    assert purchase.amount == 5000
    assert purchase.email == 'karsten@ticketfarm.de'

    assert tickets[0].secret != tickets[1]

    purchase_tickets = sorted([t.id for t in purchase.tickets])
    assert purchase_tickets == ticket_ids

    assert tickets[0].event.id == event.id
    assert tickets[1].event.id == event.id


def test_ticket_of(database):
    event = Event.create(price=2500, title='METZ', description='at Logo')
    purchase = Purchase.create(email='karsten@ticketfarm.de', event=event)
    tickets = purchase.create_tickets(2)

    selected = Ticket.of(tickets[0].id, tickets[0].secret)
    assert selected.event.id == event.id

    with pytest.raises(Ticket.DoesNotExist):
        Ticket.of(42, 'notsosecret')
