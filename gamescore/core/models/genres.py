from gamescore.core.models.associations import UserGameGenre
from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship
from sqlmodel import Field

class Genre(BaseModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    user_id: int = Field(foreign_key="users.id")  # жанр всегда принадлежит пользователю
    # Ссылка на связь с таблицей UserGameGenre
    user_games: list["UserGame"] = Relationship(back_populates="genres", link_model=UserGameGenre)