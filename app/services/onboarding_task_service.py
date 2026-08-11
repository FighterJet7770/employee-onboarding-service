"""Onboarding task business service."""

from app.models.onboarding_task import OnboardingTask
from app.repositories.onboarding_task_repository import OnboardingTaskRepository


class OnboardingTaskService:
    """Use-cases for onboarding task master data."""

    def __init__(self, repository: OnboardingTaskRepository) -> None:
        self.repository = repository

    def list_tasks(self) -> list[OnboardingTask]:
        return self.repository.list_all()

    def create_task(self, code: str, title: str, description: str | None) -> OnboardingTask:
        return self.repository.create(code=code, title=title, description=description)
