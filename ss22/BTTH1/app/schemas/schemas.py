from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int


class LoginRequest(UserBase):
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ProfileResponse(BaseModel):
    message: str