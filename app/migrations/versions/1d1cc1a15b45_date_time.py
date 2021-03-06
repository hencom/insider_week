"""date time

Revision ID: 1d1cc1a15b45
Revises: fc2aa9c95f05
Create Date: 2022-06-20 14:03:26.253759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d1cc1a15b45'
down_revision = 'fc2aa9c95f05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'date')
    # ### end Alembic commands ###
