from peewee import (CharField, ForeignKeyField, IntegerField, TextField)
import secrets
from tickets.app import db


class Event(db.Model):
    price = IntegerField()
    title = TextField()
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
        return [
            Ticket.create(event=self.event, purchase=self)
            for _ in range(count)
        ]

    @classmethod
    def of(cls, purchase_id, secret):
        return Purchase.select().where((Purchase.id == purchase_id) &
                                       (Purchase.secret == secret)).get()


class Ticket(db.Model):
    event = ForeignKeyField(Event, related_name='messages')
    purchase = ForeignKeyField(Purchase, related_name='tickets')
    secret = CharField(default=secrets.token_hex)

    @classmethod
    def of(cls, ticket_id, secret):
        return cls.select().where((Ticket.id == ticket_id) &
                                  (Ticket.secret == secret)).get()
