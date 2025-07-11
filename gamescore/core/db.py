from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from gamescore.core.models import db_helper  # ваш DataBaseHelper


# Получаем стандартную сессию нашей главной БД \ Нужно чтобы при желании перезаписать эту зависимость.
async def get_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield session