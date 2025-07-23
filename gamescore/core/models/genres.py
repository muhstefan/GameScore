from sqlalchemy import UniqueConstraint
from gamescore.core.models import UserGameGenre
from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship
from sqlmodel import Field
from typing import Optional


class Genre(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="users.id")

    user: "User" = Relationship(back_populates="genres")

    user_game_genres: list["UserGameGenre"] = Relationship(
        back_populates="genre",
        sa_relationship_kwargs={"overlaps": "user_games"}
    )

    user_games: list["UserGame"] = Relationship(
        back_populates="genres",
        link_model=UserGameGenre,
        sa_relationship_kwargs={"overlaps": "user_game_genres,user_game"}
    )

    __table_args__ = (
        UniqueConstraint("user_id", "id", name="uq_user_genre_name"),
    )