from typing import Optional
from sqlmodel import Field, Relationship
from pydantic import ConfigDict
from gamescore.core.models.base import BaseModel
from gamescore.core.models.users import UserGame, GameStatus


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
    user_games: list["UserGame"] = Relationship(back_populates="game")

class GameCreate(GameBase):
    pass

class GameRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class UserGameRead(BaseModel):
    id: int
    status: GameStatus
    rating: Optional[int]
    game: GameRead
    model_config = ConfigDict(from_attributes=True)


class GameUpdate(BaseModel):
    name: Optional[str] = None  #Значения по умолчанию None - обнулит поле например при полном обновлении
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None
