class BaseAppException(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BaseCustomException(Exception):
    """Base custom exception with error code and details."""
    def __init__(
        self, 
        message: str, 
        status_code: int = 400,
        error_code: str = "BAD_REQUEST",
        details: dict = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)
