"""Onboarding progress business service."""

from app.exceptions.custom import NotFoundException
from app.models.document_submission import DocumentStatus, DocumentSubmission
from app.models.employee_task import EmployeeTask, TaskProgressStatus
from app.repositories.document_submission_repository import DocumentSubmissionRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.employee_task_repository import EmployeeTaskRepository
from app.repositories.onboarding_task_repository import OnboardingTaskRepository


class ProgressService:
    """Use-cases for task progress and document status tracking."""

    def __init__(
        self,
        employee_repository: EmployeeRepository,
        task_repository: OnboardingTaskRepository,
        employee_task_repository: EmployeeTaskRepository,
        document_repository: DocumentSubmissionRepository,
    ) -> None:
        self.employee_repository = employee_repository
        self.task_repository = task_repository
        self.employee_task_repository = employee_task_repository
        self.document_repository = document_repository

    def update_task_status(
        self,
        employee_id: int,
        task_id: int,
        status: TaskProgressStatus,
    ) -> EmployeeTask:
        if self.employee_repository.get_by_id(employee_id) is None:
            raise NotFoundException(f"Employee with id={employee_id} not found")
        if self.task_repository.get_by_id(task_id) is None:
            raise NotFoundException(f"Task with id={task_id} not found")

        return self.employee_task_repository.upsert_status(
            employee_id=employee_id,
            task_id=task_id,
            status=status,
        )

    def upsert_document(
        self,
        employee_id: int,
        document_type: str,
        reference_id: str,
        status: DocumentStatus,
    ) -> DocumentSubmission:
        if self.employee_repository.get_by_id(employee_id) is None:
            raise NotFoundException(f"Employee with id={employee_id} not found")

        return self.document_repository.upsert(
            employee_id=employee_id,
            document_type=document_type,
            reference_id=reference_id,
            status=status,
        )

    def get_checklist_progress(self, employee_id: int) -> dict[str, int | float]:
        if self.employee_repository.get_by_id(employee_id) is None:
            raise NotFoundException(f"Employee with id={employee_id} not found")

        tasks = self.employee_task_repository.list_by_employee(employee_id)
        total = len(tasks)
        completed = sum(1 for task in tasks if task.status == TaskProgressStatus.completed)
        percent = (completed / total * 100) if total > 0 else 0.0

        return {
            "employee_id": employee_id,
            "total_tasks": total,
            "completed_tasks": completed,
            "completion_percent": round(percent, 2),
        }
