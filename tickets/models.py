from peewee import (CharField, ForeignKeyField, IntegerField, TextField)
import secrets
import stripe
from tickets.app import (db, mail)
from tickets.tools import external_url_for


class Event(db.Model):
    price = IntegerField()
    title = TextField()
    description = TextField()

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
        assert count > 0
        return [Ticket.create(event=self.event, purchase=self) for _ in range(count)]

    @property
    def amount(self):
        ''' Calculate amount for purcahse.'''
        return self.event.price * len(self.tickets)

    @property
    def description(self):
        ''' Descripe purchase.'''
        ticket_count = len(self.tickets)
        return "Your purchase of {} tickets for {}".format(ticket_count, self.event.title)

    @property
    def subject(self):
        ticket_count = len(self.tickets)
        if ticket_count == 1:
            return "Your 1 ticket for {}".format(self.event.title)
        return "Your {} tickets for {}".format(ticket_count, self.event.title)

    @property
    def body(self):
        url = external_url_for('purchase', purchase_id=self.id, secret=self.secret)
        return """Thanks for your purchase!

You can download your tickets under: {url}.

-Your Ticketfarm Team
""".format(url=url)

    def charge(self, token):
        ''' Call Stripe to make a charge for this purchase.'''
        stripe.Charge.create(
            amount=self.amount,
            currency='eur',
            source=token,
            description=self.description,
            metadata={
                'purchase_id': self.id
            })

    def notify(self):
        mail.send(self.email, self.subject, self.body)

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
        return cls.select().where((Ticket.id == ticket_id) & (Ticket.secret == secret)).get()
