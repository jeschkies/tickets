from flask import Flask
import os
from peewee import Model, SqliteDatabase
from playhouse.pool import PooledPostgresqlExtDatabase
from raven.contrib.flask import Sentry
import stripe
from urllib.parse import urlparse
from tickets.mail import (Postmark, TestMailer)

app = Flask(__name__)
app.config.from_object('tickets.config.default')
app.config.from_object(os.getenv('TICKETFARM_SETTINGS', 'tickets.config.default'))

# Stripe
stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY', None),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY', None)
}

stripe.api_key = stripe_keys['secret_key']

if app.config['MAIL_ENGINE'] == 'mail.Postmark':
    mail = Postmark(os.environ.get('POSTMARK_API_TOKEN', 'POSTMARK_API_TEST'))
else:
    mail = TestMailer()

# Sentry
# DSN is provided by environment variable `SENTRY_DSN`.
if app.config['SENTRY_ENABLED']:
    sentry = Sentry(app)


# Database
class Database(object):
    def __init__(self, app):
        self.db_engine = self.sqlite() if self.is_sqlite() else self.postgres()
        self.Model = self.get_model_class()

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.db_engine

        return BaseModel

    def is_sqlite(self):
        return app.config['DB_ENGINE'] == 'peewee.SqliteDatabase'

    def sqlite(self):
        return SqliteDatabase(app.config['DB_NAME'])

    def postgres(self):
        assert app.config['DB_ENGINE'] == 'peewee.PostgresqlDatabase'
        db_url = urlparse(os.environ.get('DATABASE_URL', None))
        database = db_url.path[1:]
        return PooledPostgresqlExtDatabase(
            database,
            max_connections=1,
            stale_timeout=300,  # 5 minutes
            timeout=0,  # Wait forever for a connection
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            register_hstore=False)


db = Database(app)


@app.before_request
def connect_db():
    if db.db_engine.is_closed():
        db.db_engine.connect()


@app.teardown_appcontext
def close_db(error):
    db.db_engine.close()
