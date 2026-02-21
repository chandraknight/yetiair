"""DTOs for flight-related operations."""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class FlightAvailabilityDTO:
    """Internal DTO for flight availability data."""
    search_id: str
    origin: str
    destination: str
    depart_date: str
    return_date: Optional[str]
    adults: int
    children: int
    infants: int
    others: int
    nationality: str


@dataclass
class FlightAddDTO:
    """Internal DTO for adding flight to booking."""
    search_id: str
    flight_id: str
    fare_id: str
    origin: str
    destination: str
    adults: int
    children: int
    infants: int


@dataclass
class ServiceResponseDTO:
    """Generic service response DTO."""
    search_id: str
    data: Optional[Dict[str, Any]] = None
    raw_response: Optional[str] = None
