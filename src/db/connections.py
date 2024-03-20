from typing import Union, Dict, Optional

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def get_db_connection_url(
        username: Optional[str],
        password: Optional[str],
        host: Optional[str],
        port: Optional[int],
        database: Optional[str]
) -> URL:
    """Получить URL подключения к БД касс"""
    return URL.create(
        drivername="postgresql+asyncpg",
        username=username,
        password=password,
        host=host,
        port=port,
        database=database
    )


def create_engine_by_url(
        url: Union[URL, str]
) -> AsyncEngine:
    """Получить async engine sqlalchemy для работы с БД по URL"""
    return create_async_engine(url=url)


class EngineStorage:
    """Хранилище engine sqlalchemy"""

    def __init__(self):
        self._storage: Dict[URL, AsyncEngine] = dict()

    def _get_engine_by_url(self, url: URL) -> AsyncEngine:
        engine = self._storage.get(url)
        if engine is None:
            engine = create_engine_by_url(url)
            self._storage[url] = engine

        return engine

    def get_engine_by_url(self, url: URL) -> AsyncEngine:
        """Получить engine по URL"""
        engine = self._get_engine_by_url(url)
        return engine

    def get_engine(
            self,
            username: str,
            password: str,
            host: str,
            port: int,
            database: str
    ) -> AsyncEngine:
        """Получить engine по параметрам"""
        url = get_db_connection_url(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        engine = self._get_engine_by_url(url)
        return engine
