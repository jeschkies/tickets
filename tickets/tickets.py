from flask import Flask, redirect, render_template, request, url_for
import os
import stripe
import uuid

app = Flask(__name__)

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

class Ticket(object):
    def __init__(self, event_id, ticket_id, email):
        self.__event_id = event_id
        self.id = ticket_id
        self.__email = email

class Purchase(object):
    def __init__(self, purchase_id, tickets):
        self.id = purchase_id
        self.tickets = tickets

class Event(object):
    def __init__(self, event_id):
        self.price = 2500
        self.__id = event_id
        self.__tickets = list()

    def add_ticket(self, ticket):
        self.__tickets.append(ticket)


events = {'1': Event(1)}
purchases = {}

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
    # Charge money
    charge = stripe.Charge.create(
        amount=amount,
        currency='eur',
        source=token
    )

    # Create tickets
    tickets = [Ticket(event_id, uuid.uuid4(), email) for _ in range(ticket_count)]
    purchase = Purchase(1, tickets)
    purchases['1'] = purchase
    for ticket in tickets:
        event.add_ticket(ticket)

    # TODO: create purchase id
    print(events)
    return redirect(url_for('purchase', purchase_id=purchase.id), code=302)

@app.route("/purchase/<purchase_id>")
def purchase(purchase_id):
    purchase = purchases[purchase_id]
    return render_template('purchase.html', purchase=purchase)

if __name__ == "__main__":
    app.run()
