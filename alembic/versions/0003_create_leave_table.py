"""create leave requests table

Revision ID: 0003_create_leave_table
Revises: 0002_create_attendance_table
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_create_leave_table"
down_revision: Union[str, Sequence[str], None] = "0002_create_attendance_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leaves",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("leave_type", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_leaves_employee_id", "leaves", ["employee_id"], unique=False)
    op.create_index("ix_leaves_leave_type", "leaves", ["leave_type"], unique=False)
    op.create_index("ix_leaves_start_date", "leaves", ["start_date"], unique=False)
    op.create_index("ix_leaves_end_date", "leaves", ["end_date"], unique=False)
    op.create_index("ix_leaves_status", "leaves", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_leaves_status", table_name="leaves")
    op.drop_index("ix_leaves_end_date", table_name="leaves")
    op.drop_index("ix_leaves_start_date", table_name="leaves")
    op.drop_index("ix_leaves_leave_type", table_name="leaves")
    op.drop_index("ix_leaves_employee_id", table_name="leaves")
    op.drop_table("leaves")
