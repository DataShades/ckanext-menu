"""Add translations column

Revision ID: bf99daca3cec
Revises: 94a7d1b465b2
Create Date: 2025-07-19 23:25:23.502560

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'bf99daca3cec'
down_revision = '94a7d1b465b2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "menu_item",
        sa.Column(
            "translations", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )


def downgrade():
    op.drop_column("menu_item", "translations")