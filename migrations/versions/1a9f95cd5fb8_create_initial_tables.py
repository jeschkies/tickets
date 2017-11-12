"""create initial tables

Revision ID: 1a9f95cd5fb8
Revises: 
Create Date: 2017-10-24 20:11:47.499354+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1a9f95cd5fb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('event',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('price', sa.Integer, nullable=False),
                    sa.Column('title', sa.Unicode(200), nullable=False),
                    sa.Column('description', sa.Text, nullable=False))

    op.create_table('purchase',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column(
                        'event_id',
                        sa.Integer,
                        sa.ForeignKey('event.id'),
                        nullable=False),
                    sa.Column('email', sa.Text, nullable=False),
                    sa.Column('secret', sa.String, nullable=False))
    op.create_index('purchase_event_id', 'purchase', ['event_id'])

    op.create_table('ticket',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column(
                        'event_id',
                        sa.Integer,
                        sa.ForeignKey('event.id'),
                        nullable=False),
                    sa.Column(
                        'purchase_id',
                        sa.Integer,
                        sa.ForeignKey('purchase.id'),
                        nullable=False),
                    sa.Column('secret', sa.String, nullable=False))
    op.create_index('ticket_event_id', 'ticket', ['event_id'])
    op.create_index('ticket_purchase_id', 'ticket', ['purchase_id'])


def downgrade():
    op.drop_table('event')

    op.drop_table('purchase')
    op.drop_index('purchase_event_id')

    op.drop_table('ticket')
    op.drop_index('ticket_event_id')
    op.drop_index('ticket_purchase_id')
