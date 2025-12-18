from pydantic import BaseModel

class ProviderServiceCreate(BaseModel):
    provider_id: int
    service_id: int
    price: int
    availability: bool
