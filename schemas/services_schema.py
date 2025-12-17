from pydantic import BaseModel

class ServiceCreate(BaseModel):
    name: str
    price : int
    description: str
    