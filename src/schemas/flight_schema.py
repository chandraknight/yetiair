from pydantic import BaseModel
from typing import Optional, List

class FlightAvailabilityRequest(BaseModel):
    origin: str
    destination: str
    depart_date: str  # Format: YYYYMMDD
    return_date: Optional[str] = None
    adults: int = 1
    children: int = 0
    infants: int = 0
    others: int = 0
    nationality: str = "NP"

class FlightAvailabilityResponse(BaseModel):
    search_id: str
    raw_response: str
    data: Optional[dict] = None
