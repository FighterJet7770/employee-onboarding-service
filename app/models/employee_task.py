"""Employee task progress ORM model."""

import enum

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TaskProgressStatus(str, enum.Enum):
    """Task status in onboarding checklist."""

    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class EmployeeTask(Base):
    """Task assignment and progress for an employee."""

    __tablename__ = "employee_tasks"
    __table_args__ = (
        UniqueConstraint("employee_id", "task_id", name="uq_employee_tasks_employee_task"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("onboarding_tasks.id"), nullable=False)
    status: Mapped[TaskProgressStatus] = mapped_column(
        Enum(TaskProgressStatus), default=TaskProgressStatus.not_started, nullable=False
    )

    employee = relationship("Employee", back_populates="tasks")
    task = relationship("OnboardingTask", back_populates="employee_tasks")
