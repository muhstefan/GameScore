from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship
from sqlmodel import Field
from enum import Enum


class UserGameGenre(BaseModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    game_id: int = Field(foreign_key="games.id", primary_key=True)
    genre_id: int = Field(foreign_key="genres.id", primary_key=True)

class GameStatus(str, Enum):
    done = "done"
    wait = "wait"

class UserGame(BaseModel, table=True):

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    game_id: int = Field(foreign_key="games.id", primary_key=True)
    status: GameStatus = Field(default=GameStatus.wait)
    rating: int | None = Field(default=None, ge=1, le=10)
    genre_id: int | None = Field(foreign_key="genres.id")

    # Ссылка на связь с таблицей UserGameGenre
    genres: list["Genre"] = Relationship(back_populates="user_games", link_model=UserGameGenre)