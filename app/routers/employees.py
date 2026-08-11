"""Employee API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeStatusUpdate
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Build employee service dependency."""
    return EmployeeService(
        employee_repository=EmployeeRepository(db),
        department_repository=DepartmentRepository(db),
    )


@router.get("", response_model=list[EmployeeRead])
def list_employees(service: EmployeeService = Depends(get_employee_service)) -> list[EmployeeRead]:
    """List employees."""
    return service.list_employees()


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    """Create employee profile."""
    return service.create_employee(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=str(payload.email),
        department_id=payload.department_id,
    )


@router.patch("/{employee_id}/status", response_model=EmployeeRead)
def update_employee_status(
    employee_id: int,
    payload: EmployeeStatusUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeRead:
    """Update employee onboarding lifecycle status."""
    return service.update_employee_status(employee_id=employee_id, new_status=payload.status)
