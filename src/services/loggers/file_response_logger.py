"""File-based response logger implementation."""
from typing import Any
from pydantic import BaseModel
from src.services.interfaces.response_logger import IResponseLogger
from src.modules.yeti_client import yeti_client


class FileResponseLogger(IResponseLogger):
    """Logger that writes responses to files."""
    
    def log_response(self, search_id: str, filename: str, content: Any) -> None:
        """Log response to file using yeti_client."""
        try:
            if isinstance(content, BaseModel):
                json_content = content.model_dump_json(indent=2)
            elif isinstance(content, str):
                json_content = content
            else:
                json_content = str(content)
            
            yeti_client.log_to_file(search_id, filename, json_content)
        except Exception:
            # Silently fail if logging fails
            pass
