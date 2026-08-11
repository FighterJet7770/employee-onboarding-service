"""Onboarding task API router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.onboarding_task_repository import OnboardingTaskRepository
from app.schemas.onboarding_task import OnboardingTaskCreate, OnboardingTaskRead
from app.services.onboarding_task_service import OnboardingTaskService

router = APIRouter(prefix="/onboarding-tasks", tags=["onboarding-tasks"])


def get_onboarding_task_service(db: Session = Depends(get_db)) -> OnboardingTaskService:
    """Build onboarding task service dependency."""
    return OnboardingTaskService(OnboardingTaskRepository(db))


@router.get("", response_model=list[OnboardingTaskRead])
def list_tasks(service: OnboardingTaskService = Depends(get_onboarding_task_service)) -> list[OnboardingTaskRead]:
    """List onboarding tasks."""
    return service.list_tasks()


@router.post("", response_model=OnboardingTaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: OnboardingTaskCreate,
    service: OnboardingTaskService = Depends(get_onboarding_task_service),
) -> OnboardingTaskRead:
    """Create onboarding task master."""
    return service.create_task(code=payload.code, title=payload.title, description=payload.description)
