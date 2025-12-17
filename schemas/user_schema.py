from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    address : str
    role: str
    