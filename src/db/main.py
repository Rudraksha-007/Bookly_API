from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from src.config import setting
from sqlmodel import SQLModel
from src.db.models import Book
from typing import AsyncGenerator

engine: AsyncEngine = create_async_engine(
    url=setting.DATABASE_URL
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Specify the session class
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    print("Connecting...")
    async with async_session() as session:
        yield session