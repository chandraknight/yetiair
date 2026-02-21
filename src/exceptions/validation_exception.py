"""Validation specific exceptions."""
from src.exceptions.base_exception import BaseCustomException


class ValidationException(BaseCustomException):
    """Exception raised for validation errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details
        )


class ServiceUnavailableException(BaseCustomException):
    """Exception raised when external service is unavailable."""
    def __init__(self, message: str = "Service temporarily unavailable", details: dict = None):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
            details=details
        )
