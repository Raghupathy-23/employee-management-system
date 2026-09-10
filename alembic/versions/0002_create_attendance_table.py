"""create attendance table

Revision ID: 0002_create_attendance_table
Revises: 0001_create_core_tables
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_create_attendance_table"
down_revision: Union[str, Sequence[str], None] = "0001_create_core_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("check_in", sa.DateTime(), nullable=True),
        sa.Column("check_out", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="uq_attendance_employee_date",
        ),
    )

    op.create_index(
        "ix_attendance_employee_id", "attendance", ["employee_id"], unique=False
    )
    op.create_index(
        "ix_attendance_attendance_date",
        "attendance",
        ["attendance_date"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_status", "attendance", ["status"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_attendance_status", table_name="attendance")
    op.drop_index("ix_attendance_attendance_date", table_name="attendance")
    op.drop_index("ix_attendance_employee_id", table_name="attendance")
    op.drop_table("attendance")
