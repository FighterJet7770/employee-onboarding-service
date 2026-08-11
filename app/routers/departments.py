"""Department API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["departments"])


def get_department_service(db: Session = Depends(get_db)) -> DepartmentService:
    """Build department service dependency."""
    return DepartmentService(DepartmentRepository(db))


@router.get("", response_model=list[DepartmentRead])
def list_departments(service: DepartmentService = Depends(get_department_service)) -> list[DepartmentRead]:
    """List all departments."""
    return service.list_departments()


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    service: DepartmentService = Depends(get_department_service),
) -> DepartmentRead:
    """Create a new department."""
    return service.create_department(name=payload.name, description=payload.description)


@router.patch("/{department_id}", response_model=DepartmentRead)
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    service: DepartmentService = Depends(get_department_service),
) -> DepartmentRead:
    """Update department details."""
    return service.update_department(
        department_id=department_id,
        name=payload.name,
        description=payload.description,
    )


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    service: DepartmentService = Depends(get_department_service),
) -> None:
    """Delete an existing department."""
    service.delete_department(department_id=department_id)
