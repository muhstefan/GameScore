from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class UserBase(SQLModel):
    login: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(..., max_length=25)


class UserCreate(UserBase):
    password: str = Field(..., max_length=25)


class UserUpdate(SQLModel):
    login: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=25)
    password: Optional[str] = Field(default=None, max_length=25)


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
