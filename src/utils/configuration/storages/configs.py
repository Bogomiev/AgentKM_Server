import enum
from pathlib import Path
from typing import Dict, Optional, Any, Callable, Union, TypeVar

from src.utils.configuration.environment.exceptions import BaseEnvironmentException
from src.utils.configuration.environment.utils import EnvironmentUtils
from src.utils.configuration.storages.exceptions import NotFoundConfigLoaderByExtensionException, \
    NoKeyValueConfigStorageException
from src.utils.configuration.storages.loaders.base import ConfigLoader
from src.utils.configuration.storages.loaders.env import EnvConfigLoader
from src.utils.configuration.storages.loaders.yaml import YamlConfigLoader

FuncResult = TypeVar("FuncResult")
ConfigValue = Union[str, int, float]
ChangedConfigValue = Union[ConfigValue, FuncResult]


class ConfigLoaderChoice(enum.IntEnum):
    YAML = enum.auto()
    ENV = enum.auto()


class ConfigStorage:
    """Хранилище конфигурационных данных"""

    _loaders = {
        ConfigLoaderChoice.YAML: YamlConfigLoader(),
        ConfigLoaderChoice.ENV: EnvConfigLoader()
    }

    def __init__(self, data: Dict[str, Optional[str]]):
        self._data = data

    @classmethod
    def _get_loader_by_path(cls, path: Path) -> ConfigLoader:
        if path.suffix in (".yml", ".yaml"):
            loader_choice = ConfigLoaderChoice.YAML
        elif path.name.startswith(".env") or "env" in path.name.split("."):
            loader_choice = ConfigLoaderChoice.ENV
        else:
            raise NotFoundConfigLoaderByExtensionException

        loader = cls._loaders.get(loader_choice)
        if loader is None:
            raise NotFoundConfigLoaderByExtensionException

        return loader

    @classmethod
    def _update_data_by_path(cls, data: dict, path: Path):
        loader = cls._get_loader_by_path(path)

        data_part = loader.load(path)

        data_keys_cross = set(data.keys()) & set(data_part.keys())

        data.update(data_part)

    @classmethod
    def create(cls, *paths: Union[str, Path]) -> 'ConfigStorage':
        data = dict()

        for path in paths:
            if isinstance(path, str):
                path = Path(path)

            cls._update_data_by_path(data, path)

        return cls(data)

    def _get_value_from_storage(self, key: str) -> Optional[ConfigValue]:
        return self._data.get(key)

    @staticmethod
    def _get_value_from_environment(key: str) -> Optional[str]:
        try:
            value = EnvironmentUtils.get_env_value(key)
        except BaseEnvironmentException:
            value = None

        return value

    def _get_value(
            self,
            key: str,
            *,
            default: Optional[Any],
            func: Optional[Callable[..., FuncResult]]
    ) -> ConfigValue:
        value = self._get_value_from_storage(key)
        if value is None:
            value = self._get_value_from_environment(key)

        if (value is not None) and (func is not None):
            value = func(value)

        if value is None:
            if default is not None:
                value = default
            else:
                raise NoKeyValueConfigStorageException(f"Нет значения конфигурации с именем {key}")

        return value

    def get(
            self,
            key: str,
            *,
            default: Optional[Any] = None,
            func: Optional[Callable[..., FuncResult]] = None
    ) -> ChangedConfigValue:
        """
        Получить значение

        :param key: имя переменной окружения
        :param default: значение по умолчанию
        :param func: функция, которую нужно применить к результату
        :return: значение переменной окружения
        :raises NoKeyValueConfigStorageException: если нет переменной окружения с именем `key`
        """
        return self._get_value(key, default=default, func=func)
