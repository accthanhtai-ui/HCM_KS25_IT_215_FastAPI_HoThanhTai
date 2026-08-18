from pydantic import BaseModel

class UserRequestDTo(BaseModel):
    name: str
    email: str
