from pydantic import BaseModel
from datetime import date


class ProviderCreate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    dob: date
    address: str
    service_id: int
    years_experience: int
    specialization: str
    bio: str
    id_proof: str
    certificate: str

class ProviderLogin(BaseModel):
    email: str
    password: str


class ProviderUpdate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    dob: date
    address: str
    service_id: int
    years_experience: int
    specialization: str
    bio: str
    id_proof: str
    certificate: str
    is_verified: bool


class ProviderResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str
    dob: date
    address: str
    service_id: int
    years_experience: int
    specialization: str
    bio: str
    id_proof: str
    certificate: str
    role: str
    is_verified: bool

    class Config:
        from_attributes = True
