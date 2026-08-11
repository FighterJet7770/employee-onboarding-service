"""Onboarding task DTOs."""

from pydantic import BaseModel, Field


class OnboardingTaskCreate(BaseModel):
    """Payload to create an onboarding task."""

    code: str = Field(min_length=2, max_length=50)
    title: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class OnboardingTaskRead(BaseModel):
    """Serialized onboarding task."""

    id: int
    code: str
    title: str
    description: str | None

    model_config = {"from_attributes": True}
