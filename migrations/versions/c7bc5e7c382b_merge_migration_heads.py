"""merge migration heads

Revision ID: c7bc5e7c382b
Revises: 3546e42b6d9f, 5c0fb96fc2b4
Create Date: 2026-06-17 14:34:45.064145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7bc5e7c382b'
down_revision = ('3546e42b6d9f', '5c0fb96fc2b4')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
