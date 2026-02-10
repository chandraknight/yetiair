from pydantic import BaseModel
from typing import Optional

class FlightAddRequest(BaseModel):
    search_id: str
    flight_id: str
    fare_id: Optional[str] = ""
    origin: str
    destination: str
    adults: int = 1
    children: int = 0
    infants: int = 0

class FlightAddResponse(BaseModel):
    search_id: str
    raw_response: str
