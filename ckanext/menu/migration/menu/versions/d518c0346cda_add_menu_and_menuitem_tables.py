"""Add menu and menu_item tables

Revision ID: d518c0346cda
Revises:
Create Date: 2025-06-24 21:29:36.388627

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d518c0346cda"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "menu",
        sa.Column("id", sa.Integer, primary_key=True, unique=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False, unique=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "menu_item",
        sa.Column("id", sa.Integer, primary_key=True, unique=True, autoincrement=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("order", sa.Integer, nullable=False, default=0),
        sa.Column("pid", sa.Text, nullable=True),
        sa.Column("mid", sa.Integer, sa.ForeignKey("menu.id"), nullable=False),
        sa.Column("classes", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("menu_item")
    op.drop_table("menu")
