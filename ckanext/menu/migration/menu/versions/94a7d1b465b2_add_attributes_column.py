"""Add attributes column

Revision ID: 94a7d1b465b2
Revises: d518c0346cda
Create Date: 2025-06-27 11:24:50.974534

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "94a7d1b465b2"
down_revision = "d518c0346cda"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "menu_item",
        sa.Column("attributes", sa.Text()),
    )


def downgrade():
    op.drop_column("menu_item", "attributes")
