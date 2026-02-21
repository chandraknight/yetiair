"""Interface for response logging."""
from abc import ABC, abstractmethod
from typing import Any


class IResponseLogger(ABC):
    """Interface for logging service responses."""
    
    @abstractmethod
    def log_response(self, search_id: str, filename: str, content: Any) -> None:
        """Log response to file."""
        pass
