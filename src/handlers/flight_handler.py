import uuid
from fastapi import APIRouter, HTTPException, Request
from src.schemas.flight_schema import FlightAvailabilityRequest, FlightAvailabilityResponse
from src.services.flight_service_facade import flight_service_facade
from src.logger import get_search_logger
from src.middleware.rate_limiter import limiter

from src.schemas.service_schema import ServiceResponse
from src.schemas.flight_add_schema import FlightAddRequest, FlightAddResponse
from src.schemas.booking_session_schema import BookingSessionRequest, BookingSessionResponse
from src.schemas.booking_save_schema import BookingSaveRequest, BookingSaveResponse
from src.schemas.itinerary_schema import ItineraryRequest, ItineraryResponse

router = APIRouter(prefix="/flights", tags=["flights"])

@router.post("/availability", response_model=FlightAvailabilityResponse)
@limiter.limit("20/minute")
async def check_availability(http_request: Request, request: FlightAvailabilityRequest):
    """
    Check flight availability with rate limiting (20 requests/minute).
    """
    search_id = str(uuid.uuid4())
    logger = get_search_logger(search_id)
    
    logger.info(f"Received flight availability request: {request}")
    try:
        response = await flight_service_facade.check_availability(request, search_id)
        logger.info("Successfully processed flight availability request")
        return response
    except Exception as e:
        logger.error(f"Error processing flight availability request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/init", response_model=ServiceResponse)
@limiter.limit("30/minute")
async def service_initialize(http_request: Request):
    """
    Initialize service with rate limiting (30 requests/minute).
    """
    search_id = str(uuid.uuid4())
    logger = get_search_logger(search_id)
    
    logger.info(f"Received ServiceInitialize request")
    try:
        response_text = await flight_service_facade.initialize_service(search_id)
        logger.info("Successfully processed ServiceInitialize request")
        return ServiceResponse(search_id=search_id, raw_response=response_text)
    except Exception as e:
        logger.error(f"Error processing ServiceInitialize request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add", response_model=FlightAddResponse)
@limiter.limit("30/minute")
async def add_flight(http_request: Request, request: FlightAddRequest):
    """
    Add flight to booking with rate limiting (30 requests/minute).
    """
    # Use the search_id from the request to continue the session/log trail
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received FlightAdd request: {request}")
    try:
        response = await flight_service_facade.add_flight(request, search_id)
        logger.info("Successfully processed FlightAdd request")
        return response
    except Exception as e:
        logger.error(f"Error processing FlightAdd request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/booking-session", response_model=BookingSessionResponse)
@limiter.limit("50/minute")
async def get_booking_session(http_request: Request, request: BookingSessionRequest):
    """
    Get booking session with rate limiting (50 requests/minute).
    """
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingGetSession request: {request}")
    try:
        response = await flight_service_facade.get_booking_session(request)
        logger.info("Successfully processed BookingGetSession request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingGetSession request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", response_model=BookingSaveResponse)
@limiter.limit("10/minute")
async def save_booking(http_request: Request, request: BookingSaveRequest):
    """
    Save booking with strict rate limiting (10 requests/minute).
    This is a critical operation with lower limits.
    """
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingSave request: {request}")
    try:
        response = await flight_service_facade.save_booking(request)
        logger.info("Successfully processed BookingSave request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingSave request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/itinerary", response_model=ItineraryResponse)
@limiter.limit("50/minute")
async def get_itinerary(http_request: Request, request: ItineraryRequest):
    """
    Get booking itinerary with rate limiting (50 requests/minute).
    """
    search_id = request.search_id
    logger = get_search_logger(search_id)
    
    logger.info(f"Received BookingGetItinerary request: {request}")
    try:
        response = await flight_service_facade.get_itinerary(request)
        logger.info("Successfully processed BookingGetItinerary request")
        return response
    except Exception as e:
        logger.error(f"Error processing BookingGetItinerary request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
