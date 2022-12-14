"""added user phone number

Revision ID: 141eddd7ba8e
Revises: f732c6f5fe9b
Create Date: 2022-09-13 16:29:03.221795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '141eddd7ba8e'
down_revision = 'f732c6f5fe9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
