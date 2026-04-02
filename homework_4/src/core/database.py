from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from core.config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
