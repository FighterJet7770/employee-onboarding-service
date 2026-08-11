"""Department business service."""

from app.exceptions.custom import NotFoundException
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository


class DepartmentService:
    """Use-cases for department lifecycle management."""

    def __init__(self, repository: DepartmentRepository) -> None:
        self.repository = repository

    def list_departments(self) -> list[Department]:
        return self.repository.list_all()

    def create_department(self, name: str, description: str | None) -> Department:
        return self.repository.create(name=name, description=description)

    def update_department(
        self,
        department_id: int,
        name: str | None,
        description: str | None,
    ) -> Department:
        department = self.repository.get_by_id(department_id)
        if department is None:
            raise NotFoundException(f"Department with id={department_id} not found")
        return self.repository.update(department=department, name=name, description=description)

    def delete_department(self, department_id: int) -> None:
        department = self.repository.get_by_id(department_id)
        if department is None:
            raise NotFoundException(f"Department with id={department_id} not found")
        self.repository.delete(department)
