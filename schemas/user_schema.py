from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    address: str


class UserLogin(BaseModel):
    email: str
    password: str

