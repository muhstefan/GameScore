from gamescore.core.models.base import BaseModel
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)
    password_hash: str
    role: str = Field(default="user")

    genres: List["Genre"] = Relationship(back_populates="user")
    user_games: List["UserGame"] = Relationship(back_populates="user")

class UserGameGenre(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_game_id: int = Field(foreign_key="usergames.id")  # Имя таблицы в нижнем регистре
    genre_id: int = Field(foreign_key="genres.id")

    user_game: Optional["UserGame"] = Relationship(back_populates="user_game_genres",
                                                   sa_relationship_kwargs={"overlaps": "genres"})
    genre: Optional["Genre"] = Relationship(back_populates="user_game_genres",
                                            sa_relationship_kwargs={"overlaps": "user_games"})


class GameStatus(str, Enum):
    wait = "wait"
    done = "done"

class UserGame(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    game_id: int = Field(foreign_key="games.id")

    status: GameStatus = Field(default=GameStatus.wait)
    rating: Optional[int] = Field(default=None, ge=1, le=10)
    review: Optional[str] = Field(default=None)

    user: "User" = Relationship(back_populates="user_games")
    game: "Game" = Relationship(back_populates="user_games")

    genres: List["Genre"] = Relationship(
        back_populates="user_games",
        link_model=UserGameGenre,
        sa_relationship_kwargs={"overlaps": "user_game,user_game_genres,genre"}
    )
    user_game_genres: List["UserGameGenre"] = Relationship(
        back_populates="user_game",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
            "overlaps": "genres"
        }
    )

