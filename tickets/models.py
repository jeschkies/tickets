from peewee import (CharField, ForeignKeyField, IntegerField, TextField)
import secrets
import stripe
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
        ''' Create one more ticket for purchase.'''
        return Ticket.create(event=self.event, purchase=self)

    def create_tickets(self, count):
        ''' Create tickets for purchase.'''
        return [
            Ticket.create(event=self.event, purchase=self)
            for _ in range(count)
        ]

    def amount(self):
        ''' Calculate amount for purcahse.'''
        return self.event.price * len(self.tickets)

    def description(self):
        ''' Descripe purchase.'''
        ticket_count = len(self.tickets)
        return "Your purchase of {} tickets for METZ".format(ticket_count)

    def charge(self, token):
        ''' Call Stripe to make a charge for this purchase.'''
        stripe.Charge.create(
            amount=self.amount(),
            currency='eur',
            source=token,
            description=self.description(),
            metadata={
                'purchase_id': self.id
            })

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
