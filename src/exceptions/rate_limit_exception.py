"""Rate limit specific exceptions."""
from src.exceptions.base_exception import BaseCustomException


class RateLimitException(BaseCustomException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", details: dict = None):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )
