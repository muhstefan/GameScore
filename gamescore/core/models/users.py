from typing import Optional
from pydantic import ConfigDict
from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship ,Field
from enum import Enum


class UserBase(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)


class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    role: str = Field(default="user")

    genres: list["Genre"] = Relationship(back_populates="user")
    user_games: list["UserGame"] = Relationship(back_populates="user")

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

# ТАБЛИЦЫ СВЯЗЕЙ

class GameStatus(str, Enum):
    done = "done"
    wait = "wait"

class UserGameGenre(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_game_id: int = Field(foreign_key="usergames.id")
    genre_id: int = Field(foreign_key="genres.id")

    user_game: Optional["UserGame"] = Relationship(
        back_populates="user_game_genres",
        sa_relationship_kwargs={"overlaps": "genres"}
    )
    genre: Optional["Genre"] = Relationship(
        back_populates="user_game_genres",
        sa_relationship_kwargs={"overlaps": "user_games"}
    )


# Добавление игр к пользователю
class UserGame(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    game_id: int = Field(foreign_key="games.id")

    status: GameStatus = Field(default=GameStatus.wait)
    rating: Optional[int] = Field(default=None, ge=1, le=10)

    user: "User" = Relationship(back_populates="user_games")

    genres: list["Genre"] = Relationship(
        back_populates="user_games",
        link_model=UserGameGenre,
        sa_relationship_kwargs={"overlaps": "user_game,user_game_genres,genre"}
    )

    user_game_genres: list["UserGameGenre"] = Relationship(
        back_populates="user_game",
        sa_relationship_kwargs={"overlaps": "genres"}
    )
