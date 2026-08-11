"""Employee business service."""

from app.exceptions.custom import NotFoundException, ValidationException
from app.models.employee import Employee, EmployeeStatus
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository

VALID_STATUS_TRANSITIONS: dict[EmployeeStatus, set[EmployeeStatus]] = {
    EmployeeStatus.draft: {EmployeeStatus.in_progress, EmployeeStatus.rejected},
    EmployeeStatus.in_progress: {EmployeeStatus.completed, EmployeeStatus.rejected},
    EmployeeStatus.completed: set(),
    EmployeeStatus.rejected: set(),
}


class EmployeeService:
    """Use-cases for employee onboarding lifecycle."""

    def __init__(
        self,
        employee_repository: EmployeeRepository,
        department_repository: DepartmentRepository,
    ) -> None:
        self.employee_repository = employee_repository
        self.department_repository = department_repository

    def list_employees(self) -> list[Employee]:
        return self.employee_repository.list_all()

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
    ) -> Employee:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise ValidationException(f"Invalid department_id={department_id}")

        return self.employee_repository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
        )

    def update_employee_status(self, employee_id: int, new_status: EmployeeStatus) -> Employee:
        employee = self.employee_repository.get_by_id(employee_id)
        if employee is None:
            raise NotFoundException(f"Employee with id={employee_id} not found")

        allowed = VALID_STATUS_TRANSITIONS.get(employee.status, set())
        if new_status not in allowed:
            raise ValidationException(
                f"Invalid status transition from {employee.status} to {new_status}"
            )

        return self.employee_repository.update_status(employee=employee, status=new_status)
