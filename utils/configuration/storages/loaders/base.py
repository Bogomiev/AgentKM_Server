import abc
from pathlib import Path


class ConfigLoader(abc.ABC):
    """Абстрактный класс загрузчика конфигурационных данных"""

    @abc.abstractmethod
    def load(self, path: Path) -> dict:
        """Загрузить конфигурационные данные из файла"""
