from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict

class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None


class GameCreate(GameBase):
    pass

class GameRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class GameUpdate(BaseModel):
    name: Optional[str] = None  #Значения по умолчанию None - обнулит поле например при полном обновлении
    description: Optional[str] = None
    rating: Optional[int] = None
    image: Optional[str] = None