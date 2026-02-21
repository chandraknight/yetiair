"""Service for flight availability operations."""
from src.dtos.flight_dto import FlightAvailabilityDTO, ServiceResponseDTO
from src.modules.yeti_client import yeti_client
from src.services.interfaces.response_parser import IResponseParser
from src.services.interfaces.response_logger import IResponseLogger
from src.schemas.flight_schema import FlightAvailabilityRequest


class FlightAvailabilityService:
    """Handles flight availability checks with single responsibility."""
    
    def __init__(self, parser: IResponseParser, logger: IResponseLogger):
        self._parser = parser
        self._logger = logger
    
    async def check_availability(
        self, 
        request: FlightAvailabilityRequest, 
        search_id: str
    ) -> ServiceResponseDTO:
        """Check flight availability."""
        # Get raw response from external service
        raw_response = await yeti_client.get_flight_availability(request, search_id)
        
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
            "FlightAvailability_Response.json",
            response_dto
        )
        
        return response_dto
