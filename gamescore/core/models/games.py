from typing import Optional
from sqlmodel import Field
from pydantic import ConfigDict
from gamescore.core.models.base import BaseModel


class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None

class Game(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None

    # обратная связь с UserGame т.е по ИГРЕ найти пользователей у которых она добавлена
    # user_games: list["UserGame"] = Relationship(back_populates="game")

class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    name: Optional[str] = None  #Значения по умолчанию None - обнулит поле например при полном обновлении
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None

class GameRead(GameBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
