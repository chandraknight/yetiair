"""Facade for flight services - provides unified interface."""
from src.services.flight_availability_service import FlightAvailabilityService
from src.services.flight_add_service import FlightAddService
from src.services.booking_service import BookingService
from src.services.service_initialization_service import ServiceInitializationService
from src.services.parsers.xml_response_parser import XmlResponseParser
from src.services.loggers.file_response_logger import FileResponseLogger

from src.schemas.flight_schema import FlightAvailabilityRequest, FlightAvailabilityResponse
from src.schemas.flight_add_schema import FlightAddRequest, FlightAddResponse
from src.schemas.booking_session_schema import BookingSessionRequest, BookingSessionResponse
from src.schemas.booking_save_schema import BookingSaveRequest, BookingSaveResponse
from src.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse
from src.schemas.service_schema import ServiceResponse


class FlightServiceFacade:
    """
    Facade pattern to provide a unified interface to flight services.
    Coordinates between multiple specialized services.
    """
    
    def __init__(self):
        # Initialize dependencies
        parser = XmlResponseParser()
        logger = FileResponseLogger()
        
        # Initialize specialized services
        self._availability_service = FlightAvailabilityService(parser, logger)
        self._flight_add_service = FlightAddService(parser, logger)
        self._booking_service = BookingService()
        self._init_service = ServiceInitializationService()
    
    async def check_availability(
        self, 
        request: FlightAvailabilityRequest, 
        search_id: str
    ) -> FlightAvailabilityResponse:
        """Check flight availability."""
        dto = await self._availability_service.check_availability(request, search_id)
        return FlightAvailabilityResponse(search_id=dto.search_id, data=dto.data)
    
    async def initialize_service(self, search_id: str) -> str:
        """Initialize service."""
        return await self._init_service.initialize(search_id)
    
    async def add_flight(
        self, 
        request: FlightAddRequest, 
        search_id: str
    ) -> FlightAddResponse:
        """Add flight to booking."""
        dto = await self._flight_add_service.add_flight(request, search_id)
        return FlightAddResponse(search_id=dto.search_id, data=dto.data)
    
    async def get_booking_session(
        self, 
        request: BookingSessionRequest
    ) -> BookingSessionResponse:
        """Get booking session."""
        dto = await self._booking_service.get_session(request)
        return BookingSessionResponse(
            search_id=dto.search_id, 
            raw_response=dto.raw_response
        )
    
    async def save_booking(self, request: BookingSaveRequest) -> BookingSaveResponse:
        """Save booking."""
        dto = await self._booking_service.save_booking(request)
        return BookingSaveResponse(
            search_id=dto.search_id, 
            raw_response=dto.raw_response
        )
    
    async def get_itinerary(self, request: ItineraryRequest) -> ItineraryResponse:
        """Get booking itinerary."""
        dto = await self._booking_service.get_itinerary(request)
        return ItineraryResponse(
            search_id=dto.search_id, 
            raw_response=dto.raw_response
        )


# Singleton instance
flight_service_facade = FlightServiceFacade()
