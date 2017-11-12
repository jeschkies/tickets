from flask import Flask
import os
from peewee import Model, PostgresqlDatabase, SqliteDatabase
import stripe
from urllib.parse import urlparse

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
        if app.config['DB_ENGINE'] == 'peewee.SqliteDatabase':
            self.db = SqliteDatabase(app.config['DB_NAME'])
        elif app.config['DB_ENGINE'] == 'peewee.PostgresqlDatabase':
            db_url = urlparse(os.environ.get('DATABASE_URL', None))
            database = db_url.path[1:]
            self.db = PostgresqlDatabase(
                database,
                user=db_url.username,
                password=db_url.password,
                host=db_url.hostname,
                port=db_url.port)
        self.db.connect()

        self.Model = self.get_model_class()

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.db

        return BaseModel


db = Database(app)
