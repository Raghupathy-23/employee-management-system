"""add leave approval fields

Revision ID: 0004_add_leave_approval_fields
Revises: 0003_create_leave_table
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_add_leave_approval_fields"
down_revision = "0003_create_leave_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("leaves", sa.Column("approver_user_id", sa.Integer(), nullable=True))
    op.add_column("leaves", sa.Column("approval_comment", sa.Text(), nullable=True))
    op.create_index("ix_leaves_approver_user_id", "leaves", ["approver_user_id"], unique=False)
    op.create_foreign_key(
        "fk_leaves_approver_user_id_users",
        "leaves",
        "users",
        ["approver_user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_leaves_approver_user_id_users", "leaves", type_="foreignkey")
    op.drop_index("ix_leaves_approver_user_id", table_name="leaves")
    op.drop_column("leaves", "approval_comment")
    op.drop_column("leaves", "approver_user_id")
