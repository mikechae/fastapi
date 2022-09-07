"""create posts table

Revision ID: 53acff50300b
Revises: 
Create Date: 2022-09-05 16:24:48.820928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53acff50300b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
