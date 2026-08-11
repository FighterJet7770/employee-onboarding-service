"""Unit tests for employee service."""

from unittest.mock import Mock

import pytest

from app.exceptions.custom import NotFoundException, ValidationException
from app.models.employee import EmployeeStatus
from app.services.employee_service import EmployeeService


class DummyEmployee:
    def __init__(self, status: EmployeeStatus) -> None:
        self.status = status



def test_update_employee_status_raises_for_missing_employee() -> None:
    employee_repo = Mock()
    employee_repo.get_by_id.return_value = None
    service = EmployeeService(employee_repository=employee_repo, department_repository=Mock())

    with pytest.raises(NotFoundException):
        service.update_employee_status(employee_id=999, new_status=EmployeeStatus.completed)



def test_update_employee_status_rejects_invalid_transition() -> None:
    employee_repo = Mock()
    employee_repo.get_by_id.return_value = DummyEmployee(status=EmployeeStatus.draft)
    service = EmployeeService(employee_repository=employee_repo, department_repository=Mock())

    with pytest.raises(ValidationException):
        service.update_employee_status(employee_id=1, new_status=EmployeeStatus.completed)



def test_update_employee_status_allows_valid_transition() -> None:
    employee_repo = Mock()
    employee_repo.get_by_id.return_value = DummyEmployee(status=EmployeeStatus.draft)
    employee_repo.update_status.return_value = DummyEmployee(status=EmployeeStatus.in_progress)
    service = EmployeeService(employee_repository=employee_repo, department_repository=Mock())

    result = service.update_employee_status(
        employee_id=1,
        new_status=EmployeeStatus.in_progress,
    )

    assert result.status == EmployeeStatus.in_progress
