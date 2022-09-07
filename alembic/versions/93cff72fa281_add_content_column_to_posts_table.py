"""add content column to posts table

Revision ID: 93cff72fa281
Revises: 53acff50300b
Create Date: 2022-09-05 16:41:39.699021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93cff72fa281'
down_revision = '53acff50300b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
