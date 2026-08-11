"""Document submission ORM model."""

import enum

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DocumentStatus(str, enum.Enum):
    """Verification status of submitted documents."""

    pending = "pending"
    verified = "verified"
    rejected = "rejected"


class DocumentSubmission(Base):
    """Document metadata and verification status."""

    __tablename__ = "document_submissions"
    __table_args__ = (
        UniqueConstraint("employee_id", "document_type", name="uq_document_employee_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(80), nullable=False)
    reference_id: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus), default=DocumentStatus.pending, nullable=False
    )

    employee = relationship("Employee", back_populates="documents")
