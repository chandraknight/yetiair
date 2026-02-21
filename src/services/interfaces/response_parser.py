"""Interface for response parsing."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class IResponseParser(ABC):
    """Interface for parsing external service responses."""
    
    @abstractmethod
    def parse(self, raw_response: str) -> Dict[str, Any]:
        """Parse raw response to structured data."""
        pass
