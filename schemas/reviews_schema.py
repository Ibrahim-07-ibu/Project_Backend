from pydantic import BaseModel

class ReviewCreate(BaseModel):
    user_id: int
    provider_id: int
    service_id:int
    rating_service : int
    rating_provider : int 
    comment: str
