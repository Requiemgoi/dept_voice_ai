from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db


async def get_database() -> AsyncSession:
    """
    Dependency для получения сессии БД.
    """
    async for session in get_db():
        yield session

