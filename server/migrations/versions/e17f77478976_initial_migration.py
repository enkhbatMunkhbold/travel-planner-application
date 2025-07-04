"""Initial migration

Revision ID: e17f77478976
Revises: 
Create Date: 2025-06-07 17:49:08.025779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e17f77478976'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itineraries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trip_title', sa.String(length=100), nullable=False),
    sa.Column('trip_length', sa.Integer(), nullable=False),
    sa.Column('trip_route', sa.Text(), nullable=False),
    sa.Column('trip_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tours',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tour_title', sa.String(length=100), nullable=False),
    sa.Column('tour_description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tour_title')
    )
    op.create_table('travelers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(length=30), nullable=False),
    sa.Column('lname', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_of_travelers', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.Column('tour_id', sa.Integer(), nullable=False),
    sa.Column('itinerary_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], name=op.f('fk_bookings_itinerary_id_itineraries')),
    sa.ForeignKeyConstraint(['tour_id'], ['tours.id'], name=op.f('fk_bookings_tour_id_tours')),
    sa.ForeignKeyConstraint(['traveler_id'], ['travelers.id'], name=op.f('fk_bookings_traveler_id_travelers')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('travelers')
    op.drop_table('tours')
    op.drop_table('itineraries')
    # ### end Alembic commands ###
