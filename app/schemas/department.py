"""Department DTOs."""

from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    """Payload to create a department."""

    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class DepartmentUpdate(BaseModel):
    """Payload to update a department."""

    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class DepartmentRead(BaseModel):
    """Serialized department representation."""

    id: int
    name: str
    description: str | None

    model_config = {"from_attributes": True}
