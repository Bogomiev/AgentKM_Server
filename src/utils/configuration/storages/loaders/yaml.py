from pathlib import Path

import yaml

from yaml import Loader

from src.utils.configuration.storages.loaders.base import ConfigLoader


class YamlConfigLoader(ConfigLoader):
    """Загрузчик конфигурационных данных из yaml файла"""

    def load(self, path: Path) -> dict:
        with path.open("r") as f:
            return yaml.load(f, Loader=Loader)
