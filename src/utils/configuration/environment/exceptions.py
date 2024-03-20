class BaseEnvironmentException(Exception):
    """Базовое исключение приложения работы с окружением"""


class NoEnvironmentException(BaseEnvironmentException):
    """Не удалось получить значение окружения"""
