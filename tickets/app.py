from flask import Flask
import os
from peewee import Model, SqliteDatabase
import stripe

app = Flask(__name__)
app.config.from_object('tickets.config.default')
app.config.from_object(
    os.getenv('TICKETFARM_SETTINGS', 'tickets.config.default'))

stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY', None),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY', None)
}

stripe.api_key = stripe_keys['secret_key']


class Database(object):
    def __init__(self, app):
        self.db = SqliteDatabase(app.config['DB_NAME'])
        self.Model = self.get_model_class()

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.db

        return BaseModel


db = Database(app)
