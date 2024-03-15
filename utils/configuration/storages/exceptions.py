class BaseConfigStorageException(Exception):
    """Базовое исключение приложения хранилища конфигурационных данных"""


class NoKeyValueConfigStorageException(BaseConfigStorageException):
    """Не удалось получить значение из хранилища"""


class NotFoundConfigLoaderByExtensionException(BaseConfigStorageException):
    """Не удалось получить loader по расширению конфигурационного файла"""
