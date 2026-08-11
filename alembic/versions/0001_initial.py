"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-08-05
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.UniqueConstraint("name", name="uq_departments_name"),
    )

    op.create_table(
        "onboarding_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.UniqueConstraint("code", name="uq_onboarding_tasks_code"),
    )

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("status", sa.Enum("draft", "in_progress", "completed", "rejected", name="employeestatus"), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "employee_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum("not_started", "in_progress", "completed", "blocked", name="taskprogressstatus"), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["onboarding_tasks.id"]),
        sa.UniqueConstraint("employee_id", "task_id", name="uq_employee_tasks_employee_task"),
    )

    op.create_table(
        "document_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("document_type", sa.String(length=80), nullable=False),
        sa.Column("reference_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.Enum("pending", "verified", "rejected", name="documentstatus"), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.UniqueConstraint("employee_id", "document_type", name="uq_document_employee_type"),
    )


def downgrade() -> None:
    op.drop_table("document_submissions")
    op.drop_table("employee_tasks")
    op.drop_table("employees")
    op.drop_table("onboarding_tasks")
    op.drop_table("departments")
