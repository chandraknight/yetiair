from pydantic import BaseModel

class ServiceResponse(BaseModel):
    search_id: str
    raw_response: str
