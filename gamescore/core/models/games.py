from typing import Optional, TYPE_CHECKING
from sqlmodel import Field
from pydantic import ConfigDict
from gamescore.core.models.associations import UserGame
from gamescore.core.models.base import BaseModel
from sqlmodel import Relationship




class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None



class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None

    # Обратная связь many-to-many с пользователями
    users: list["User"] = Relationship(back_populates="games", link_model=UserGame)


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
