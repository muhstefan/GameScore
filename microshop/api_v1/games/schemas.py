"""
Pydantic-схемы
Это схемы валидации и сериализации данных.
"""

from pydantic import BaseModel, ConfigDict


class GameBase(BaseModel):
    name: str
    description: str
    rating : int

class GameCreate(GameBase):
    pass

class GameUpdate(GameCreate):
    pass

class GameUpdatePartical(GameCreate):
    name: str | None = None
    description: str | None = None
    rating: int | None = None

class Game(GameBase):
    model_config = ConfigDict(from_attributes=True)
    id : int

