from src.modules.yeti_client import yeti_client
from src.schemas.flight_schema import FlightAvailabilityRequest, FlightAvailabilityResponse
from src.schemas.flight_add_schema import FlightAddRequest, FlightAddResponse
from src.schemas.booking_session_schema import BookingSessionRequest, BookingSessionResponse
from src.schemas.booking_save_schema import BookingSaveRequest, BookingSaveResponse
from src.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse

from src.utils.xml_parser import parse_yeti_xml_response

class FlightService:
    @staticmethod
    async def check_availability(request: FlightAvailabilityRequest, search_id: str) -> FlightAvailabilityResponse:
        response_text = await yeti_client.get_flight_availability(request, search_id)
        # Parse XML to JSON
        parsed_data = parse_yeti_xml_response(response_text)
        
        # Create response model
        response_model = FlightAvailabilityResponse(search_id=search_id, data=parsed_data)
        
        # Log final JSON response
        try:
            # Using model_dump_json for Pydantic v2
            json_content = response_model.model_dump_json(indent=2)
            yeti_client.log_to_file(search_id, "FlightAvailability_Response.json", json_content)
        except Exception:
            # Fallback or pass silently if logging fails
            pass
            
        return response_model

    @staticmethod
    async def initialize_service(search_id: str) -> str:
        response_text = await yeti_client.service_initialize(search_id)
        return response_text

    @staticmethod
    async def add_flight(request: FlightAddRequest, search_id: str) -> FlightAddResponse:
        response_text = await yeti_client.flight_add(request, search_id)
        # Parse XML to JSON
        parsed_data = parse_yeti_xml_response(response_text)
        
        # Create response model
        response_model = FlightAddResponse(search_id=search_id, data=parsed_data)
        
        # Log final JSON response
        try:
            json_content = response_model.model_dump_json(indent=2)
            yeti_client.log_to_file(search_id, "FlightAdd_Response.json", json_content)
        except Exception:
            pass
            
        return response_model

    @staticmethod
    async def get_booking_session(request: BookingSessionRequest) -> BookingSessionResponse:
        response_text = await yeti_client.booking_get_session(request.search_id)
        return BookingSessionResponse(search_id=request.search_id, raw_response=response_text)

    @staticmethod
    async def save_booking(request: BookingSaveRequest) -> BookingSaveResponse:
        response_text = await yeti_client.booking_save(request, request.search_id)
        return BookingSaveResponse(search_id=request.search_id, raw_response=response_text)

    @staticmethod
    async def get_itinerary(request: ItineraryRequest) -> ItineraryResponse:
        response_text = await yeti_client.booking_get_itinerary(request.pnr, request.search_id)
        return ItineraryResponse(search_id=request.search_id, raw_response=response_text)

flight_service = FlightService()
