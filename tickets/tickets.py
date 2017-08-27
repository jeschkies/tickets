from flask import Flask, render_template, request
import os
import stripe

app = Flask(__name__)

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

class Event(object):
    def __init__(self):
        self.price = 2500

events = {'1': Event()}

@app.route("/")
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'],
            amount=2500)

@app.route("/charge", methods=['POST'])
def charge():
    ticket_count = int(request.form['ticket_count'])
    event_id = request.form['event_id']
    ticket_price = events[event_id].price
    amount = ticket_count * ticket_price

    token = request.form['stripeToken']
    charge = stripe.Charge.create(
        amount=amount,
        currency='eur',
        source=token
    )

    print(request.form)
    return ''

if __name__ == "__main__":
    app.run()
