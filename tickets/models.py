from peewee import (CharField, ForeignKeyField, IntegerField, Model, TextField)
import secrets
from tickets.app import app, db


class Event(db.Model):
    price = IntegerField()
    description = TextField()

    def add_ticket(self, ticket):
        self.__tickets.append(ticket)

    def create_purchase(self, email):
        return Purchase.create(event=self, email=email)


class Purchase(db.Model):
    email = TextField()
    event = ForeignKeyField(Event, related_name='purchases')
    secret = CharField(default=secrets.token_hex)

    def create_ticket(self):
        return Ticket.create(event=self.event, purchase=self)

    def create_tickets(self, count):
        return [Ticket.create(event=self.event, purchase=self)
                for _ in range(count)]


class Ticket(db.Model):
    event = ForeignKeyField(Event, related_name='messages')
    purchase = ForeignKeyField(Purchase, related_name='tickets')
    secret = CharField(default=secrets.token_hex)
