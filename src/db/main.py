from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.sql import text
from src.config import setting

engine: AsyncEngine = create_async_engine(
    url=setting.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 'hello';"))
        print(result.all())