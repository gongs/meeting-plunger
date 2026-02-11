"""add venues and venue_participants tables

Revision ID: 20260211_venues
Revises: 20260211_users
Create Date: 2026-02-11

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260211_venues"
down_revision: str | Sequence[str] | None = "20260211_users"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "venue_participants",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("condition", sa.Integer(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("won", sa.Boolean(), nullable=False),
        sa.Column("game_over", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("venue_id", "user_id", name="uq_venue_user"),
    )
    op.create_index("ix_venue_participants_venue_id", "venue_participants", ["venue_id"], unique=False)
    op.create_index("ix_venue_participants_user_id", "venue_participants", ["user_id"], unique=False)

    op.execute(sa.text("INSERT INTO venues (name, created_at) VALUES ('默认赛场', datetime('now'))"))


def downgrade() -> None:
    op.drop_index("ix_venue_participants_user_id", table_name="venue_participants")
    op.drop_index("ix_venue_participants_venue_id", table_name="venue_participants")
    op.drop_table("venue_participants")
    op.drop_table("venues")
