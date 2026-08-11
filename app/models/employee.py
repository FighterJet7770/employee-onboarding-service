"""Employee ORM model."""

import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EmployeeStatus(str, enum.Enum):
    """Lifecycle status for employees."""

    draft = "draft"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"


class Employee(Base):
    """Represents an employee under onboarding."""

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(EmployeeStatus), default=EmployeeStatus.draft, nullable=False
    )
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)

    department = relationship("Department", back_populates="employees")
    tasks = relationship("EmployeeTask", back_populates="employee")
    documents = relationship("DocumentSubmission", back_populates="employee")
