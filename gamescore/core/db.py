from fastapi import Depends
from gamescore.core.models import db_helper  # ваш DataBaseHelper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Dict, Any, Optional
from sqlmodel import SQLModel

# Получаем стандартную сессию нашей главной БД \ Нужно чтобы при желании перезаписать эту зависимость.
async def get_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield session



ModelType = TypeVar("ModelType", bound=SQLModel)

async def get_one_by_fields(
    session: AsyncSession,
    model: Type[ModelType],
    filters: Dict[str, Any]
) -> Optional[ModelType]:
    conditions = [getattr(model, key) == value for key, value in filters.items()]
    query = select(model).where(*conditions)
    result = await session.execute(query)
    return result.scalars().first()