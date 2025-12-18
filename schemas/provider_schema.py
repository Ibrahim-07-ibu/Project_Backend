from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class ProviderBase(BaseModel):
    user_id: int
    experience: str
    location: str
    bio: Optional[str] = None
    role: Optional[str] = "provider"
    is_verified: Optional[bool] = False

class ProviderCreate(ProviderBase):
    pass

class ProviderUpdate(ProviderBase):
    pass

class ProviderResponse(ProviderBase):
    id: int

    class Config:
        from_attributes = True
