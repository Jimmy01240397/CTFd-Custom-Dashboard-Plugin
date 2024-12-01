"""add CGGC

Revision ID: 101e17c71440
Revises: 
Create Date: 2024-12-01 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '101e17c71440'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(op=None):
    op.create_table(
        "cggc_challenge",
        sa.Column("id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["id"], ["challenges.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade(op=None) -> None:
    op.drop_table("cggc_challenge")
