"""Task progress and document DTOs."""

from pydantic import BaseModel, Field

from app.models.document_submission import DocumentStatus
from app.models.employee_task import TaskProgressStatus


class EmployeeTaskStatusUpdate(BaseModel):
    """Payload to update employee task status."""

    status: TaskProgressStatus


class EmployeeTaskRead(BaseModel):
    """Serialized employee task progress."""

    id: int
    employee_id: int
    task_id: int
    status: TaskProgressStatus

    model_config = {"from_attributes": True}


class DocumentSubmissionUpsert(BaseModel):
    """Payload to submit or update onboarding document metadata."""

    document_type: str = Field(min_length=2, max_length=80)
    reference_id: str = Field(min_length=1, max_length=120)
    status: DocumentStatus = DocumentStatus.pending


class DocumentSubmissionRead(BaseModel):
    """Serialized document submission."""

    id: int
    employee_id: int
    document_type: str
    reference_id: str
    status: DocumentStatus

    model_config = {"from_attributes": True}


class ChecklistProgressRead(BaseModel):
    """Aggregated onboarding progress summary."""

    employee_id: int
    total_tasks: int
    completed_tasks: int
    completion_percent: float
