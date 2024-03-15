from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

from db.connections import EngineStorage
from settings import POSTGRES_DB_USERNAME, POSTGRES_DB_PASSWORD, POSTGRES_DB_PORT, POSTGRES_DB_HOST, POSTGRES_DB_NAME

engine: AsyncEngine = EngineStorage().get_engine(username=POSTGRES_DB_USERNAME,
                                                 password=POSTGRES_DB_PASSWORD,
                                                 port=POSTGRES_DB_PORT,
                                                 host=POSTGRES_DB_HOST,
                                                 database=POSTGRES_DB_NAME)


class SqlBase:
    __abstract__ = True


SqlBase = declarative_base(cls=SqlBase)
SqlBase.metadata = MetaData()
