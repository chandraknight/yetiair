from pydantic import BaseModel
from typing import List, Optional

class BookingHeader(BaseModel):
    contact_name: str
    contact_email: str
    phone_mobile: str
    phone_home: Optional[str] = ""
    phone_business: Optional[str] = ""

class Passenger(BaseModel):
    passenger_id: str
    passenger_type_rcd: str
    lastname: str
    firstname: str
    gender_type_rcd: str
    nationality_rcd: str
    date_of_birth: str

class Payment(BaseModel):
    form_of_payment_rcd: str
    currency_rcd: str
    payment_amount: float

class BookingSaveRequest(BaseModel):
    search_id: str
    booking_header: BookingHeader
    passengers: List[Passenger]
    payment: Payment

class BookingSaveResponse(BaseModel):
    search_id: str
    raw_response: str
