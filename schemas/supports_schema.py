from pydantic import BaseModel

class SupportCreate(BaseModel):
    user_id : int
    subject : str
    message : str
