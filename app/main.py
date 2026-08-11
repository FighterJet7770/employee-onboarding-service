"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.core.config import settings
from app.core.db import engine
from app.exceptions.handlers import register_exception_handlers
from app.models.base import Base
from app.routers import departments, employees, onboarding_tasks, progress


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(title=settings.app_name)

    Base.metadata.create_all(bind=engine)

    register_exception_handlers(app)

    app.include_router(departments.router)
    app.include_router(onboarding_tasks.router)
    app.include_router(employees.router)
    app.include_router(progress.router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
