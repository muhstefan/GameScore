from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import UniqueConstraint
from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship ,Field
from enum import Enum


class UserBase(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)


class User(UserBase, table=True):
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

class UserAccountInfo(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserPublic(BaseModel):
    id: int
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)

# ТАБЛИЦЫ СВЯЗЕЙ


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

    __table_args__ = (
        UniqueConstraint('user_game_id', 'genre_id', name='uq_user_game_genre'),
    )




# Добавление игр к пользователю

class GameStatus(str, Enum):
    wait = "wait"
    done = "done"



class UserGame(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    game_id: int = Field(foreign_key="games.id")

    status: GameStatus = Field(default=GameStatus.wait)
    rating: Optional[int] = Field(default=None, ge=1, le=10)

    user: "User" = Relationship(back_populates="user_games")
    game: "Game" = Relationship(back_populates="user_games")

    genres: list["Genre"] = Relationship(
        back_populates="user_games",
        link_model=UserGameGenre,
        sa_relationship_kwargs={"overlaps": "user_game,user_game_genres,genre"}
    )

    user_game_genres: list["UserGameGenre"] = Relationship(
        back_populates="user_game",
        sa_relationship_kwargs={"overlaps": "genres"}
    )
    __table_args__ = (
        UniqueConstraint("user_id", "game_id", name="uq_user_game"),
    )

class UserGameUpdate(BaseModel):
    status: Optional[GameStatus] = None
    rating: Optional[int] = None

class UserGameFilter(BaseModel):
    status: Optional[str] = None
    min_rating: Optional[int] = None    # Используем min_rating для фильтрации рейтинга
    genre_ids: Optional[list[int]] = None  # Используется в запросе

    model_config = {
        "from_attributes": True
    }