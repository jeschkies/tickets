from flask import Flask, redirect, render_template, request, url_for
import humanhash
from tickets import models
from tickets.models import Event, Purchase, Ticket
import os
import stripe

app = Flask(__name__)

stripe_keys = {
  'secret_key': os.environ.get('STRIPE_SECRET_KEY', None),
  'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY', None)
}

stripe.api_key = stripe_keys['secret_key']

@app.template_filter('humanize')
def humanize_filter(digest):
    return humanhash.humanize(str(digest), words=5)



@app.before_request
def before_request():
    models.db.connect()
    # TODO: Do once on startup
    models.db.create_tables([Event, Purchase, Ticket], safe=True)
    Event.create(price=2500, description='METZ at Logo')


@app.after_request
def after_request(response):
    models.db.close()
    return response


@app.route("/")
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'],
                           amount=2500)


@app.route("/charge", methods=['POST'])
def charge():
    email = request.form['stripeEmail']
    ticket_count = int(request.form['ticket_count'])
    event_id = request.form['event_id']
    event = Event.select().where(Event.id == event_id).get()
    ticket_price = event.price
    amount = ticket_count * ticket_price

    token = request.form['stripeToken']

    with models.db.atomic():
        # Create tickets
        purchase = event.create_purchase(email)
        purchase.create_tickets(ticket_count)

        # Charge money
        description = "Your purchase of {} tickets for METZ".format(
                ticket_count)
        stripe.Charge.create(
            amount=amount,
            currency='eur',
            source=token,
            description=description,
            metadata={
                'purchase_id': purchase.id
            }
        )

    return redirect(url_for('purchase', purchase_id=purchase.id), code=302)


# TODO: use secret parameter as well
@app.route("/purchase/<purchase_id>")
def purchase(purchase_id):
    purchase = Purchase.select().where(Purchase.id == purchase_id).get()
    return render_template('purchase.html', purchase=purchase)


# TODO: use secret parameter as well
@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    ticket = Ticket.select().where(Ticket.id == ticket_id).get()
    return render_template('ticket.html', ticket=ticket)


if __name__ == "__main__":
    app.run()
