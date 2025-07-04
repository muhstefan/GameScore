from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class GameBase(SQLModel):
    name: str
    description: str
    rating: int


class Game(GameBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class GameCreate(GameBase):
    pass


class GameUpdate(SQLModel):
    name: Optional[str] = None  #Значения по умолчанию None - обнулит поле например при полном обновлении
    description: Optional[str] = None
    rating: Optional[int] = None


class GameRead(GameBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
