from pydantic import BaseModel

class BookingCreate(BaseModel):
    user_id: int
    provider_id: int
    service_id: int
    address : str
    city :str
    pincode : int
    date: str
    time: str
    instructions: str
    status: str
