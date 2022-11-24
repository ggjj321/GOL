"""create table

Revision ID: ce4d576fcf6f
Revises: 
Create Date: 2022-11-19 15:24:07.423588

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce4d576fcf6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column('userID', sa.Integer, primary_key = True),
        sa.Column('userName', sa.String(255), nullable = False)
    )


def downgrade() -> None:
    op.drop_table('user')
