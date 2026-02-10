from pydantic import BaseModel

class ItineraryRequest(BaseModel):
    search_id: str
    pnr: str

class ItineraryResponse(BaseModel):
    search_id: str
    raw_response: str
