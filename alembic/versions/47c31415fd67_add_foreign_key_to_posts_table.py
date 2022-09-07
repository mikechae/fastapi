"""add foreign key to posts table

Revision ID: 47c31415fd67
Revises: fa8ac6e70336
Create Date: 2022-09-06 22:22:08.603954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47c31415fd67'
down_revision = 'fa8ac6e70336'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
