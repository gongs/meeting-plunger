"""add venue rounds and results, current_round, roll_count, finished_at

Revision ID: 20260211_rounds
Revises: 20260211_venues
Create Date: 2026-02-11

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260211_rounds"
down_revision: str | Sequence[str] | None = "20260211_venues"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("venues", sa.Column("current_round", sa.Integer(), nullable=False, server_default="1"))
    op.add_column(
        "venue_participants",
        sa.Column("roll_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("venue_participants", sa.Column("finished_at", sa.DateTime(), nullable=True))

    op.create_table(
        "venue_rounds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("venue_id", "round_number", name="uq_venue_round"),
    )
    op.create_index("ix_venue_rounds_venue_id", "venue_rounds", ["venue_id"], unique=False)

    op.create_table(
        "venue_round_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("won", sa.Boolean(), nullable=False),
        sa.Column("roll_count", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("venue_id", "round_number", "user_id", name="uq_venue_round_user"),
    )
    op.create_index("ix_venue_round_results_venue_id", "venue_round_results", ["venue_id"], unique=False)
    op.create_index("ix_venue_round_results_user_id", "venue_round_results", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_venue_round_results_user_id", table_name="venue_round_results")
    op.drop_index("ix_venue_round_results_venue_id", table_name="venue_round_results")
    op.drop_table("venue_round_results")
    op.drop_index("ix_venue_rounds_venue_id", table_name="venue_rounds")
    op.drop_table("venue_rounds")
    op.drop_column("venue_participants", "finished_at")
    op.drop_column("venue_participants", "roll_count")
    op.drop_column("venues", "current_round")
