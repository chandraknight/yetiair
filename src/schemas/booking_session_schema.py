from pydantic import BaseModel

class BookingSessionRequest(BaseModel):
    search_id: str

class BookingSessionResponse(BaseModel):
    search_id: str
    raw_response: str
