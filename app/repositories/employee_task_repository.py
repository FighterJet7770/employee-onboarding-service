"""Employee task data-access repository."""

from sqlalchemy.orm import Session

from app.models.employee_task import EmployeeTask, TaskProgressStatus


class EmployeeTaskRepository:
    """Persistence operations for employee task progress."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_employee_and_task(self, employee_id: int, task_id: int) -> EmployeeTask | None:
        return (
            self.db.query(EmployeeTask)
            .filter(EmployeeTask.employee_id == employee_id, EmployeeTask.task_id == task_id)
            .first()
        )

    def list_by_employee(self, employee_id: int) -> list[EmployeeTask]:
        return self.db.query(EmployeeTask).filter(EmployeeTask.employee_id == employee_id).all()

    def upsert_status(
        self,
        employee_id: int,
        task_id: int,
        status: TaskProgressStatus,
    ) -> EmployeeTask:
        employee_task = self.get_by_employee_and_task(employee_id, task_id)
        if employee_task is None:
            employee_task = EmployeeTask(employee_id=employee_id, task_id=task_id, status=status)
            self.db.add(employee_task)
        else:
            employee_task.status = status

        self.db.commit()
        self.db.refresh(employee_task)
        return employee_task
