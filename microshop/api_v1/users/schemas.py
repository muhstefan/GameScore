from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    login: str = Field(..., max_length=25)
    email: EmailStr = Field(..., max_length=25)

class UserCreate(UserBase):
    password: str = Field(..., max_length=25)

class UserUpdate(BaseModel):
    login: Optional[str] = Field(None, max_length=25)
    email: Optional[EmailStr] = Field(None, max_length=25)
    password: Optional[str] = Field(None, max_length=25)

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)