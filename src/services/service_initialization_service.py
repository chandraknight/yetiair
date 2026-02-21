"""Service for service initialization operations."""
from src.modules.yeti_client import yeti_client


class ServiceInitializationService:
    """Handles service initialization with single responsibility."""
    
    async def initialize(self, search_id: str) -> str:
        """Initialize service."""
        return await yeti_client.service_initialize(search_id)
