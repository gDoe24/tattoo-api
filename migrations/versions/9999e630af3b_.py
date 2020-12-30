"""empty message

Revision ID: 9999e630af3b
Revises:
Create Date: 2020-12-08 11:55:03.561674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9999e630af3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'artists', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'artists', type_='unique')
    # ### end Alembic commands ###