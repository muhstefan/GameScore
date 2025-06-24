""" SQLAlchemy Это модель базы данных.
Определяет структуру таблицы в базе данных.
Используется для работы с ORM (Object-Relational Mapping) —
то есть для создания, чтения, обновления и удаления записей в базе.
"""


from sqlalchemy.orm import Mapped
from .base import Base


class Game(Base):
    name: Mapped[str]
    description: Mapped[str]
    rating: Mapped[int]