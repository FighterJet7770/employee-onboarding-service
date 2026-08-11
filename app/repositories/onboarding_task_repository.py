"""Onboarding task data-access repository."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.custom import ConflictException
from app.models.onboarding_task import OnboardingTask


class OnboardingTaskRepository:
    """Persistence operations for onboarding task masters."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[OnboardingTask]:
        return self.db.query(OnboardingTask).order_by(OnboardingTask.code).all()

    def get_by_id(self, task_id: int) -> OnboardingTask | None:
        return self.db.query(OnboardingTask).filter(OnboardingTask.id == task_id).first()

    def create(self, code: str, title: str, description: str | None) -> OnboardingTask:
        task = OnboardingTask(code=code, title=title, description=description)
        self.db.add(task)
        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictException("Task code must be unique") from exc
