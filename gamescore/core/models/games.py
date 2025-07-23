from typing import Optional
from sqlmodel import Field, Relationship
from gamescore.core.models.base import BaseModel



class Game(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None

    # обратная связь с UserGame т.е по ИГРЕ найти пользователей у которых она добавлена
    user_games: list["UserGame"] = Relationship(back_populates="game")





