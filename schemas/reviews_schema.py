from pydantic import BaseModel, conint


class ReviewCreate(BaseModel):
    service_id: int
    provider_id: int
    rating: conint(ge=1, le=5)
    comment: str


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    provider_id: int
    service_id: int
    rating: int
    comment: str

    class Config:
        from_attributes = True
