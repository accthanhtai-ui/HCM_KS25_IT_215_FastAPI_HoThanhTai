from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    major: Optional[str] = None
    gpa: Optional[float] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    major: Optional[str] = None
    gpa: Optional[float] = None


class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True
