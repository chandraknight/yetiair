"""Service for booking operations."""
from src.dtos.booking_dto import BookingSessionDTO, BookingSaveDTO, ItineraryDTO
from src.dtos.flight_dto import ServiceResponseDTO
from src.modules.yeti_client import yeti_client
from src.schemas.booking_session_schema import BookingSessionRequest
from src.schemas.booking_save_schema import BookingSaveRequest
from src.schemas.itinerary_schema import ItineraryRequest


class BookingService:
    """Handles booking-related operations with single responsibility."""
    
    async def get_session(self, request: BookingSessionRequest) -> ServiceResponseDTO:
        """Get booking session."""
        raw_response = await yeti_client.booking_get_session(request.search_id)
        
        return ServiceResponseDTO(
            search_id=request.search_id,
            raw_response=raw_response
        )
    
    async def save_booking(self, request: BookingSaveRequest) -> ServiceResponseDTO:
        """Save booking."""
        raw_response = await yeti_client.booking_save(request, request.search_id)
        
        return ServiceResponseDTO(
            search_id=request.search_id,
            raw_response=raw_response
        )
    
    async def get_itinerary(self, request: ItineraryRequest) -> ServiceResponseDTO:
        """Get booking itinerary."""
        raw_response = await yeti_client.booking_get_itinerary(
            request.pnr, 
            request.search_id
        )
        
        return ServiceResponseDTO(
            search_id=request.search_id,
            raw_response=raw_response
        )
