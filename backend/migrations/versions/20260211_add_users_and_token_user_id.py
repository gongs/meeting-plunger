"""add users table and user_id to access_tokens

Revision ID: 20260211_users
Revises: 05c205ac6937
Create Date: 2026-02-11

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260211_users"
down_revision: str | Sequence[str] | None = "05c205ac6937"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    with op.batch_alter_table("access_tokens", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_access_tokens_user_id",
            "users",
            ["user_id"],
            ["id"],
        )
        batch_op.create_index(
            "ix_access_tokens_user_id",
            ["user_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("access_tokens", schema=None) as batch_op:
        batch_op.drop_index("ix_access_tokens_user_id", if_exists=True)
        batch_op.drop_constraint("fk_access_tokens_user_id", type_="foreignkey")
        batch_op.drop_column("user_id")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
