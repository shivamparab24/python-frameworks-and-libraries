from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base

from FastAPI.Ssali_Jonathan.CRUD.core.config import get_settings


settings = get_settings()


# Async Engine
async_engine = create_async_engine(
    settings.database_url,
    # echo = True
)

print("DB URL:", settings.database_url)


# Base (for ORM models)
Base = declarative_base()


# Session Factory
SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Initialize DB
async def init_db() -> None:
    async with async_engine.begin() as conn:
        # print(Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)


# Dependency (FastAPI)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session