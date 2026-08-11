"""Employee DTOs."""

from pydantic import BaseModel, EmailStr, Field

from app.models.employee import EmployeeStatus


class EmployeeCreate(BaseModel):
    """Payload to create employee profile."""

    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    department_id: int


class EmployeeStatusUpdate(BaseModel):
    """Payload to update employee lifecycle status."""

    status: EmployeeStatus


class EmployeeRead(BaseModel):
    """Serialized employee representation."""

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: EmployeeStatus
    department_id: int

    model_config = {"from_attributes": True}
