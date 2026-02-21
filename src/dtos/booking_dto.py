"""DTOs for booking-related operations."""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class BookingHeaderDTO:
    """Booking header information."""
    contact_name: str
    contact_email: str
    phone_mobile: str
    phone_home: Optional[str] = ""
    phone_business: Optional[str] = ""


@dataclass
class PassengerDTO:
    """Passenger information."""
    passenger_id: str
    passenger_type_rcd: str
    lastname: str
    firstname: str
    gender_type_rcd: str
    nationality_rcd: str
    date_of_birth: str


@dataclass
class PaymentDTO:
    """Payment information."""
    form_of_payment_rcd: str
    currency_rcd: str
    payment_amount: float


@dataclass
class BookingSaveDTO:
    """Complete booking save data."""
    search_id: str
    booking_header: BookingHeaderDTO
    passengers: List[PassengerDTO]
    payment: PaymentDTO


@dataclass
class BookingSessionDTO:
    """Booking session request data."""
    search_id: str


@dataclass
class ItineraryDTO:
    """Itinerary request data."""
    search_id: str
    pnr: str
