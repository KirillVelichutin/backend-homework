from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from core.config import ASYNC_DB_URL

Base = declarative_base()
engine = create_async_engine(ASYNC_DB_URL)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

# Функция, которая создает подключение к БД. Используем как зависимость
async def get_db():
    async with SessionLocal() as db:
        yield db
