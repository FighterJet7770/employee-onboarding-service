"""Onboarding task ORM model."""

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class OnboardingTask(Base):
    """Master onboarding task definition."""

    __tablename__ = "onboarding_tasks"
    __table_args__ = (UniqueConstraint("code", name="uq_onboarding_tasks_code"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    employee_tasks = relationship("EmployeeTask", back_populates="task")
