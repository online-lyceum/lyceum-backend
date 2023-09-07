"""Add breaks

Revision ID: 7d4e96978327
Revises: 9e5842fe89d7
Create Date: 2023-09-07 22:12:16.905481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d4e96978327'
down_revision = '9e5842fe89d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('breaks', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lessons', 'breaks')
    # ### end Alembic commands ###