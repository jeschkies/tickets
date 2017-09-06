from flask import redirect, render_template, request, url_for
import humanhash
import stripe
from tickets.app import app, db, stripe_keys
from tickets.models import Event, Purchase, Ticket


@app.template_filter('humanize')
def humanize_filter(digest):
    return humanhash.humanize(str(digest), words=5)


@app.before_request
def before_request():
    db.db.connect()
    # TODO: Do once on startup
    db.db.create_tables([Event, Purchase, Ticket], safe=True)

    title = "METZ in Hamburg"
    description = ("Mi, 13.12.17, 21:00 Uhr\n"
                   "Knust - Hamburg\n"
                   "Neuer Kamp 30, 20357 HAMBURG\n")
    Event.create(price=2500, title=title, description=description)


@app.after_request
def after_request(response):
    db.db.close()
    return response


@app.route("/")
def index():
    event = Event.select().where(Event.id == 1).get()
    return render_template(
        'index.html',
        key=stripe_keys['publishable_key'],
        amount=2500,
        event=event)


@app.route("/charge", methods=['POST'])
def charge():
    email = request.form['stripeEmail']
    ticket_count = int(request.form['ticket_count'])
    event_id = request.form['event_id']
    event = Event.select().where(Event.id == event_id).get()
    ticket_price = event.price
    amount = ticket_count * ticket_price

    token = request.form['stripeToken']

    with db.db.atomic():
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
            metadata={'purchase_id': purchase.id})

    redirect_url = url_for(
        'purchase', purchase_id=purchase.id, secret=purchase.secret)
    return redirect(redirect_url, code=302)


@app.route("/purchase/<purchase_id>")
def purchase(purchase_id):
    # TODO: Handle no secret or unknown purchase
    secret = request.args.get('secret')
    purchase = Purchase.select().where((Purchase.id == purchase_id) &
                                       (Purchase.secret == secret)).get()
    return render_template('purchase.html', purchase=purchase)


@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    # TODO: Handle no secret or unknown ticket
    secret = request.args.get('secret')
    ticket = Ticket.select().where((Ticket.id == ticket_id) &
                                   (Ticket.secret == secret)).get()
    return render_template('ticket.html', ticket=ticket)
