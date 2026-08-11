"""Custom exception types for application and domain errors."""

from fastapi import status


class AppException(Exception):
    """Base application exception with HTTP mapping metadata."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested entity cannot be found."""

    def __init__(self, message: str) -> None:
        super().__init__("not_found", message, status.HTTP_404_NOT_FOUND)


class ConflictException(AppException):
    """Raised when operation violates uniqueness or state constraints."""

    def __init__(self, message: str) -> None:
        super().__init__("conflict", message, status.HTTP_409_CONFLICT)


class ValidationException(AppException):
    """Raised when business validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__("validation_error", message, status.HTTP_422_UNPROCESSABLE_ENTITY)
