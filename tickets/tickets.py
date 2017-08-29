from flask import Flask, redirect, render_template, request, url_for
import os
import stripe
import uuid

app = Flask(__name__)

stripe_keys = {
  'secret_key': os.environ.get('STRIPE_SECRET_KEY', None),
  'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY', None)
}

stripe.api_key = stripe_keys['secret_key']


class Ticket(object):
    def __init__(self, event_id, ticket_id):
        self.__event_id = event_id
        self.id = ticket_id


class Purchase(object):
    def __init__(self, purchase_id, event_id, tickets, email):
        self.id = purchase_id
        self.tickets = tickets
        self.event_id = event_id
        self.email = email


class Event(object):
    def __init__(self, event_id):
        self.price = 2500
        self.__id = event_id
        self.__tickets = list()

    def add_ticket(self, ticket):
        self.__tickets.append(ticket)


events = {'1': Event(1)}
purchases = {}
tickets = {}


@app.route("/")
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'],
                           amount=2500)


@app.route("/charge", methods=['POST'])
def charge():
    email = request.form['stripeEmail']
    ticket_count = int(request.form['ticket_count'])
    event_id = request.form['event_id']
    event = events[event_id]
    ticket_price = event.price
    amount = ticket_count * ticket_price

    token = request.form['stripeToken']

    # TODO: Make charge and ticket creation and atomic operation.

    # Create tickets
    new_tickets = [Ticket(event_id, uuid.uuid4()) for _ in range(ticket_count)]
    purchase = Purchase(1, event_id, new_tickets, email)
    purchases['1'] = purchase
    for ticket in new_tickets:
        tickets[ticket.id] = ticket
        event.add_ticket(ticket)

    # Charge money
    stripe.Charge.create(
        amount=amount,
        currency='eur',
        source=token,
        metadata={
            'purchase_id': purchase.id
        }
    )

    # TODO: create purchase id
    return redirect(url_for('purchase', purchase_id=purchase.id), code=302)


@app.route("/purchase/<purchase_id>")
def purchase(purchase_id):
    purchase = purchases[purchase_id]
    return render_template('purchase.html', purchase=purchase)


@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    ticket = tickets[uuid.UUID(ticket_id)]
    return render_template('ticket.html', ticket=ticket)


if __name__ == "__main__":
    app.run()
