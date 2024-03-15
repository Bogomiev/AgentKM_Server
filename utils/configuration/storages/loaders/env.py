from pathlib import Path

from dotenv import dotenv_values

from utils.configuration.storages.loaders.base import ConfigLoader


class EnvConfigLoader(ConfigLoader):
    """Загрузчик конфигурационных данных из env файла"""

    def load(self, path: Path) -> dict:
        return dotenv_values(path)
