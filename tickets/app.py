from flask import Flask
from peewee import Model, SqliteDatabase
from tickets import config

app = Flask(__name__)
app.config.from_object(config)
app.config.from_envvar('TICKETFARM_SETTINGS')

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
