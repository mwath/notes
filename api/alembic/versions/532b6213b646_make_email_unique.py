"""make email unique

Revision ID: 532b6213b646
Revises: 668fb224d575
Create Date: 2022-09-01 02:44:53.686606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '532b6213b646'
down_revision = '668fb224d575'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###