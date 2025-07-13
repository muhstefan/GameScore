from gamescore.core.models.base import BaseModel
from sqlmodel import Field


class UserGame(BaseModel, table=True):
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    game_id: int = Field(foreign_key="games.id", primary_key=True)
