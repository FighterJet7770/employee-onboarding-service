"""Employee data-access repository."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.custom import ConflictException
from app.models.employee import Employee, EmployeeStatus


class EmployeeRepository:
    """Persistence operations for employee profiles."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Employee]:
        return self.db.query(Employee).order_by(Employee.id).all()

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        department_id: int,
    ) -> Employee:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
        )
        self.db.add(employee)
        try:
            self.db.commit()
            self.db.refresh(employee)
            return employee
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("Employee email must be unique") from exc

    def update_status(self, employee: Employee, status: EmployeeStatus) -> Employee:
        employee.status = status
        self.db.commit()
        self.db.refresh(employee)
        return employee
