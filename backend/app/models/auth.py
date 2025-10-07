from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str
    role: str = Field(default="student", regex=r"^(student|teacher|parent)$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    expires_at: datetime


class UserProfile(BaseModel):
    user_id: str
    email: EmailStr
    display_name: str
    role: str
    created_at: datetime
    streak: int
    xp: int
    current_world: str
    current_level: int
    avatar: Optional[str]
