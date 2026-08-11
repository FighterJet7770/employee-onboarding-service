"""Progress and document API router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.document_submission_repository import DocumentSubmissionRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.employee_task_repository import EmployeeTaskRepository
from app.repositories.onboarding_task_repository import OnboardingTaskRepository
from app.schemas.progress import (
    ChecklistProgressRead,
    DocumentSubmissionRead,
    DocumentSubmissionUpsert,
    EmployeeTaskRead,
    EmployeeTaskStatusUpdate,
)
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/employees", tags=["progress"])


def get_progress_service(db: Session = Depends(get_db)) -> ProgressService:
    """Build progress service dependency."""
    return ProgressService(
        employee_repository=EmployeeRepository(db),
        task_repository=OnboardingTaskRepository(db),
        employee_task_repository=EmployeeTaskRepository(db),
        document_repository=DocumentSubmissionRepository(db),
    )


@router.post("/{employee_id}/tasks/{task_id}/status", response_model=EmployeeTaskRead)
def update_task_status(
    employee_id: int,
    task_id: int,
    payload: EmployeeTaskStatusUpdate,
    service: ProgressService = Depends(get_progress_service),
) -> EmployeeTaskRead:
    """Upsert task progress status for an employee."""
    return service.update_task_status(employee_id=employee_id, task_id=task_id, status=payload.status)


@router.post("/{employee_id}/documents", response_model=DocumentSubmissionRead)
def upsert_document(
    employee_id: int,
    payload: DocumentSubmissionUpsert,
    service: ProgressService = Depends(get_progress_service),
) -> DocumentSubmissionRead:
    """Submit or update document metadata and verification status."""
    return service.upsert_document(
        employee_id=employee_id,
        document_type=payload.document_type,
        reference_id=payload.reference_id,
        status=payload.status,
    )


@router.get("/{employee_id}/checklist-progress", response_model=ChecklistProgressRead)
def get_checklist_progress(
    employee_id: int,
    service: ProgressService = Depends(get_progress_service),
) -> ChecklistProgressRead:
    """Get checklist completion summary for employee."""
    progress = service.get_checklist_progress(employee_id=employee_id)
    return ChecklistProgressRead(**progress)
