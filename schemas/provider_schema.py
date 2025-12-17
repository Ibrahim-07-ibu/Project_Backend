from pydantic import BaseModel

class ProviderCreate(BaseModel):
    user_id: int
    experience: str
    location: str
    bio: str
    role : str
    is_verified: bool
