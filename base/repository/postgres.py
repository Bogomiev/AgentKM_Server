import abc
import dataclasses
from typing import List, Any, Set, Iterable, Dict, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update
from db.postgresdb import SqlBase

Base = declarative_base()


class PostgresRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, session: AsyncSession, data, auto_commit: bool = True):
        """
        Добавляет новую запись в базу
        """

    @abc.abstractmethod
    async def update(self, session: AsyncSession, data, auto_commit: bool = True):
        """
        Обновляет существующую запись в базе
        """

    @abc.abstractmethod
    async def delete(self, session: AsyncSession, data, auto_commit: bool = True):
        """
        Удаляет запись из базы
        """

    @abc.abstractmethod
    async def add_all(self, session: AsyncSession, data: Iterable[Any], auto_commit: bool = True):
        """
        Добавляет список новых записей в базу
        """

    @abc.abstractmethod
    async def update_all(self, session: AsyncSession, data: List[Any], auto_commit: bool = True):
        """
        Обновляет список существующих записей в базе
        """

    @abc.abstractmethod
    async def save_all(self, session: AsyncSession, data: Iterable[Any], auto_commit: bool = True):
        """
        Добавляет новые записи, обновляет существующие
        """

    @abc.abstractmethod
    async def delete_all(self, session: AsyncSession, data: Iterable[Any], auto_commit: bool = True):
        """
        Удаляет список существующих записей из базы
        """


@dataclasses.dataclass
class BasePostgresRepository(PostgresRepository):
    _model: SqlBase
    _keys: Tuple[Any]
    _exclusion_fields_update: Set[str] = dataclasses.field(default_factory=frozenset)
    _partition: int = 1000

    async def add(self, session, item, auto_commit: bool = True):
        session.add(item)
        if auto_commit:
            await session.commit()

    async def update(self, session, item, auto_commit: bool = True):
        keys = frozenset(item.__dict__.keys()) - self._exclusion_fields_update - frozenset(['_sa_instance_state'])
        update_stmt = update(self._model).values(self._item_to_dict(item, keys))
        await session.execute(update_stmt)
        if auto_commit:
            await session.commit()

    async def delete(self, session, item, auto_commit: bool = True):
        await session.delete(item)
        if auto_commit:
            await session.commit()

    async def add_all(self, session, items, auto_commit: bool = True):
        session.add_all(items)
        if auto_commit:
            await session.commit()

    async def update_all(self, session, items, auto_commit: bool = True):
        for item in items:
            await self.update(session, item, auto_commit=False)
        if auto_commit:
            await session.commit()

    async def delete_all(self, session, items, auto_commit: bool = True):
        for item in items:
            await session.delete(item)
        if auto_commit:
            await session.commit()

    @staticmethod
    def _get_values_to_update_from_stmt(keys: Iterable[str], stmt):
        return {key: stmt.excluded[key] for key in keys}

    @staticmethod
    def _item_to_dict(item, keys: Iterable[str]) -> Dict:
        return {key: getattr(item, key) for key in keys}

    def _gen_records(self, items, keys: Iterable[str]):
        record_partition = []
        c = 0
        for item in items:
            record_partition.append(self._item_to_dict(item, keys))
            c += 1
            if c % self._partition == 0:
                yield record_partition
                record_partition.clear()
        yield record_partition

    async def save_all(self, session: AsyncSession, items, auto_commit: bool = True):
        if len(items) > 0:
            keys = frozenset(dict(items[0]).keys()) - self._exclusion_fields_update
            keys_update = keys - frozenset(['id'])

            for next_partition in self._gen_records(items, keys):
                if next_partition:
                    stmt = insert(self._model).values(next_partition)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=self._keys, set_=self._get_values_to_update_from_stmt(keys_update, stmt))

                    await session.execute(stmt)
            if auto_commit:
                await session.commit()
