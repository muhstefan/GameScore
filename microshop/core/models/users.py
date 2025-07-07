from typing import Optional
from sqlmodel import Field
from pydantic import ConfigDict
from microshop.core.models.base import BaseModel

class UserBase(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(...)

class UserCreate(UserBase):
    password: str = Field(...)

class UserCreateDB(UserBase):
    username: str
    email: str
    password_hash: str  # хэш пароля для базы

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=25)
    password: Optional[str] = Field(default=None, max_length=25, min_length=8)

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)