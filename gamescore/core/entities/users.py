from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from pydantic import ConfigDict
from gamescore.core.entities.games import GameRead
from gamescore.core.entities.genres import GenreRead


class UserBase(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=25)

class UserCreateDB(UserBase):
    password_hash: str

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=25)
    password: Optional[str] = Field(default=None, max_length=25, min_length=8)

class UserAccountInfo(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserPublic(BaseModel):
    id: int
    username: str
    role: str
    model_config = ConfigDict(from_attributes=True)

class GameStatus(str, Enum):
    wait = "wait"
    done = "done"

class UserGameUpdate(BaseModel):
    status: Optional[GameStatus] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    genre_ids: Optional[List[int]] = None
    model_config = ConfigDict(from_attributes=True)

class UserGameFilter(BaseModel):
    status: Optional[GameStatus] = None
    min_rating: Optional[int] = None
    genre_ids: Optional[List[int]] = None
    model_config = ConfigDict(from_attributes=True)



class UserGameRead(BaseModel):
    id: int
    status: GameStatus
    rating: Optional[int]
    review: Optional[str] = None

    game: "GameRead"
    genres: List["GenreRead"] = []

    model_config = ConfigDict(from_attributes=True)

UserGameRead.model_rebuild()