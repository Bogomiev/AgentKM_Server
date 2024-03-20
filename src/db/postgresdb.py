from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.db.connections import EngineStorage
from src.settings import (POSTGRES_DB_USERNAME, POSTGRES_DB_PASSWORD, POSTGRES_DB_PORT, POSTGRES_DB_HOST,
                          POSTGRES_DB_NAME)

engine: AsyncEngine = EngineStorage().get_engine(username=POSTGRES_DB_USERNAME,
                                                 password=POSTGRES_DB_PASSWORD,
                                                 port=POSTGRES_DB_PORT,
                                                 host=POSTGRES_DB_HOST,
                                                 database=POSTGRES_DB_NAME)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class SqlBase:
    __abstract__ = True


SqlBase = declarative_base(cls=SqlBase)
SqlBase.metadata = MetaData()
