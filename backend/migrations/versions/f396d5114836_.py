"""empty message

Revision ID: f396d5114836
Revises: 
Create Date: 2021-01-04 14:05:25.680950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f396d5114836'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('styles', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('instagram_link', sa.String(length=500), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=240), nullable=True),
    sa.Column('address', sa.String(length=240), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client', sa.Integer(), nullable=True),
    sa.Column('artist', sa.Integer(), nullable=True),
    sa.Column('appointment_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['client'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    op.drop_table('clients')
    op.drop_table('artists')
    # ### end Alembic commands ###
