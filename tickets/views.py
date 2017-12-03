from babel.numbers import format_currency
from flask import abort, redirect, render_template, request, send_file, url_for
import humanhash
from io import BytesIO
import pyqrcode
from tickets.app import app, db, stripe_keys
from tickets.models import Event, Purchase, Ticket


@app.template_filter('humanize')
def humanize_filter(digest):
    return humanhash.humanize(str(digest), words=5)


@app.template_filter('currency')
def currency_filter(cents):
    return format_currency(cents / 100, 'EUR', locale='de_DE')


@app.route("/")
def index():
    event = Event.select().where(Event.id == 1).get()
    return render_template(
        'index.html', stripe_publishable_key=stripe_keys['publishable_key'], event=event)


@app.route("/charge", methods=['POST'])
def charge():
    email = request.form['stripeEmail']
    token = request.form['stripeToken']
    ticket_count = int(request.form['ticket_count'])
    event_id = request.form['event_id']

    try:
        event = Event.select().where(Event.id == event_id).get()
    except Event.DoesNotExist:
        abort(404)

    with db.db_engine.atomic():
        # Create tickets
        purchase = event.create_purchase(email)
        purchase.create_tickets(ticket_count)

        # Charge money
        purchase.charge(token)
        purchase.notify()

    redirect_url = url_for('purchase', purchase_id=purchase.id, secret=purchase.secret)
    return redirect(redirect_url, code=302)


@app.route("/purchase/<purchase_id>")
def purchase(purchase_id):
    secret = request.args.get('secret')
    try:
        purchase = Purchase.of(purchase_id, secret)
        return render_template('purchase.html', purchase=purchase)
    except Purchase.DoesNotExist:
        abort(404)


@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    secret = request.args.get('secret')
    try:
        ticket = Ticket.of(ticket_id, secret)
        return render_template('ticket.html', ticket=ticket)
    except Ticket.DoesNotExist:
        abort(404)


@app.route("/ticket/<ticket_id>.svg")
def ticket_qrcode(ticket_id):
    secret = request.args.get('secret')
    try:
        Ticket.of(ticket_id, secret)
    except Ticket.DoesNotExist:
        abort(404)

    qr = pyqrcode.create(secret)
    out = BytesIO()
    qr.svg(out, scale=4)
    out.seek(0)
    return send_file(out, mimetype='image/svg+xml')
