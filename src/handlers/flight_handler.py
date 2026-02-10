import uuid
from fastapi import APIRouter, HTTPException
from src.schemas.flight_schema import FlightAvailabilityRequest, FlightAvailabilityResponse
from src.services.flight_service import flight_service
from src.logger import get_search_logger

from src.schemas.service_schema import ServiceResponse
from src.schemas.flight_add_schema import FlightAddRequest, FlightAddResponse
from src.schemas.booking_session_schema import BookingSessionRequest, BookingSessionResponse
from src.schemas.booking_save_schema import BookingSaveRequest, BookingSaveResponse
from src.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse

router = APIRouter(prefix="/flights", tags=["flights"])

@router.post("/availability", response_model=FlightAvailabilityResponse)
async def check_availability(request: FlightAvailabilityRequest):
    search_id = str(uuid.uuid4())
    logger = get_search_logger(search_id)
    
    logger.info(f"Received flight availability request: {request}")
    try:
        response = await flight_service.check_availability(request, search_id)
        logger.info("Successfully processed flight availability request")
        return response
    except Exception as e:
        logger.error(f"Error processing flight availability request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/init", response_model=ServiceResponse)
async def service_initialize():
    search_id = str(uuid.uuid4())
    logger = get_search_logger(search_id)
    
    logger.info(f"Received ServiceInitialize request")
    try:
        response_text = await flight_service.initialize_service(search_id)
        logger.info("Successfully processed ServiceInitialize request")
        return ServiceResponse(search_id=search_id, raw_response=response_text)
    except Exception as e:
        logger.error(f"Error processing ServiceInitialize request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add", response_model=FlightAddResponse)
async def add_flight(request: FlightAddRequest):
    # Use the search_id from the request to continue the session/log trail
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received FlightAdd request: {request}")
    try:
        response = await flight_service.add_flight(request, search_id)
        logger.info("Successfully processed FlightAdd request")
        return response
    except Exception as e:
        logger.error(f"Error processing FlightAdd request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/booking-session", response_model=BookingSessionResponse)
async def get_booking_session(request: BookingSessionRequest):
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingGetSession request: {request}")
    try:
        response = await flight_service.get_booking_session(request)
        logger.info("Successfully processed BookingGetSession request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingGetSession request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", response_model=BookingSaveResponse)
async def save_booking(request: BookingSaveRequest):
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingSave request: {request}")
    try:
        response = await flight_service.save_booking(request)
        logger.info("Successfully processed BookingSave request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingSave request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/itinerary", response_model=ItineraryResponse)
async def get_itinerary(request: ItineraryRequest):
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingGetItinerary request: {request}")
    try:
        response = await flight_service.get_itinerary(request)
        logger.info("Successfully processed BookingGetItinerary request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingGetItinerary request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
