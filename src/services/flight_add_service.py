"""Service for adding flights to booking."""
from src.dtos.flight_dto import FlightAddDTO, ServiceResponseDTO
from src.modules.yeti_client import yeti_client
from src.services.interfaces.response_parser import IResponseParser
from src.services.interfaces.response_logger import IResponseLogger
from src.schemas.flight_add_schema import FlightAddRequest


class FlightAddService:
    """Handles adding flights to booking with single responsibility."""
    
    def __init__(self, parser: IResponseParser, logger: IResponseLogger):
        self._parser = parser
        self._logger = logger
    
    async def add_flight(
        self, 
        request: FlightAddRequest, 
        search_id: str
    ) -> ServiceResponseDTO:
        """Add flight to booking."""
        # Get raw response from external service
        raw_response = await yeti_client.flight_add(request, search_id)
        
        # Parse response
        parsed_data = self._parser.parse(raw_response)
        
        # Create DTO
        response_dto = ServiceResponseDTO(
            search_id=search_id,
            data=parsed_data
        )
        
        # Log response
        self._logger.log_response(
            search_id,
            "FlightAdd_Response.json",
            response_dto
        )
        
        return response_dto
