from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreateAdmin(UserCreate):
    role: Role


class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: Role
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
