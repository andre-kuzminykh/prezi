"""
Custom application exceptions with HTTP status code mapping.

## Traceability
- Feature: F000 (Application Bootstrap)
"""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str = "An application error occurred", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)


class ValidationError(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message=message, status_code=422)
