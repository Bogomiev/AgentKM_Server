import os
from pathlib import Path
from typing import Union

from utils import server
from utils.configuration.environment.exceptions import BaseEnvironmentException
from utils.configuration.environment.utils import EnvironmentUtils
from utils.configuration.storages.configs import ConfigStorage


class Config:
    # наименования переменных окружения путей к конфиг файлам
    _general_config_name = "GENERAL_CONFIG_FILE"
    _config_name = "CONFIG_FILE"

    _general_env_name = "GENERAL_ENV_FILE"
    _env_name = "ENV_FILE"

    # пути к конфиг файлам по умолчанию
    _general_config = "configs/app.yml"
    _dev_config = "configs/app.dev.yml"
    _prod_config = "configs/app.prod.yml"

    _general_env = ".envs/.env"
    _dev_env = ".envs/.env.dev"
    _prod_env = ".envs/.env.prod"

    def __init__(self, root_dir: Union[str, Path]):
        self.root_dir = root_dir

    def _abs_path(self, path):
        if not os.path.isabs(path):
            path = os.path.join(self.root_dir, path)

        return path

    def _get_general_config_path(self):
        path = EnvironmentUtils.get_env_value(self._general_config_name,
                                              default=self._general_config)
        path = self._abs_path(path)
        return path

    def _get_config_path(self):
        try:
            path = EnvironmentUtils.get_env_value(self._config_name)
        except BaseEnvironmentException:
            if server.is_dev() or server.is_local_dev():
                path = self._dev_config
            elif server.is_production():
                path = self._prod_config
            else:
                raise Exception("Не удалось найти конфигурационный файл приложения")

        path = self._abs_path(path)
        return path

    def _get_general_env_path(self):
        path = EnvironmentUtils.get_env_value(self._general_env_name,
                                              default=self._general_env)
        path = self._abs_path(path)
        return path

    def _get_env_path(self):
        try:
            path = EnvironmentUtils.get_env_value(self._env_name)
        except BaseEnvironmentException:
            if server.is_dev() or server.is_local_dev():
                path = self._dev_env
            elif server.is_production():
                path = self._prod_env
            else:
                raise Exception("Не удалось найти файл с secrets для приложения")

        path = self._abs_path(path)
        return path

    def _get_paths(self):
        return (
            self._get_general_config_path(),
            self._get_config_path(),
            self._get_general_env_path(),
            self._get_env_path(),
        )

    def get_config_storage(self):
        """
        Получить хранилище конфигурации

        Получение путей конфиг файлам построенна следующим образом:

        - Определяется путь к основному конфиг файлу (общие данные для dev и prod)
        - Определяется путь к dev/prod конфиг файлу (данные специфичные для dev и prod)
        - Определяется путь к основному файлу секретов (общие данные для dev и prod)
        - Определяется путь к dev/prod файлу секретов (данные специфичные для dev и prod)

        Для определения в каком режиме (dev или prod) запущен сервер используются функции модуля `core.srv.utils.server`

        Чтоб напрямую указать, какие конфигурационные файлы использовать (без использования
        автоматического определения dev/prod), необходимо задать переменные окружения:

        - основной конфиг файл: GENERAL_CONFIG_FILE
        - dev/prod конфиг файл: CONFIG_FILE
        - основной файл с секретами: GENERAL_ENV_FILE
        - dev/prod файл с секретами: ENV_FILE

        Для тех файлов, для которых переменная окружения не установлена будет использовано автоматическое определение.

        Пример использования для принудительного запуска в prod режиме на локальной машине:
            CONFIG_FILE=configs/app.prod.yml

            ENV_FILE=.envs/.env.prod

        P.S.:
            В идеале стоит сделать переключение dev/prod режим более удобным
        """
        paths = self._get_paths()
        return ConfigStorage.create(*paths)
