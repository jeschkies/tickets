from flask import Flask
import os
from peewee import Model, SqliteDatabase
from tickets import config

app = Flask(__name__)
app.config.from_object(config)
app.config.from_json(os.environ['TICKETFARM_SETTINGS'])


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
