"""Department data-access repository."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.custom import ConflictException
from app.models.department import Department


class DepartmentRepository:
    """Department persistence operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Department]:
        return self.db.query(Department).order_by(Department.name).all()

    def get_by_id(self, department_id: int) -> Department | None:
        return self.db.query(Department).filter(Department.id == department_id).first()

    def create(self, name: str, description: str | None) -> Department:
        department = Department(name=name, description=description)
        self.db.add(department)
        try:
            self.db.commit()
            self.db.refresh(department)
            return department
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("Department name must be unique") from exc

    def update(self, department: Department, name: str | None, description: str | None) -> Department:
        if name is not None:
            department.name = name
        if description is not None:
            department.description = description
        try:
            self.db.commit()
            self.db.refresh(department)
            return department
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("Department update violates constraints") from exc

    def delete(self, department: Department) -> None:
        self.db.delete(department)
        self.db.commit()
