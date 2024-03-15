import os
from typing import Optional, Any, List, Callable, TypeVar, Union

from utils.configuration.environment.exceptions import NoEnvironmentException

FuncResult = TypeVar("FuncResult")


class EnvironmentUtils:
    """Класс для удобной работы с переменными окружения"""

    @classmethod
    def get_env_value(
            cls,
            key: str,
            *,
            default: Optional[Any] = None,
            func: Optional[Callable[..., FuncResult]] = None
    ) -> Union[str, FuncResult]:
        """
        Получить значение окружения

        :param key: имя переменной окружения
        :param default: значение по умолчанию
        :param func: функция, которую нужно применить к результату
        :return: значение переменной окружения
        :raises NoEnvironmentException: если нет переменной окружения с именем `key`
        """
        value = os.getenv(key)
        if value is None and default is None:
            raise NoEnvironmentException(f"Нет переменной окружения с именем {key}")
        elif value is None and default is not None:
            return default

        if func is not None:
            value = func(value)

        return value

    @classmethod
    def get_env_sep_values(
            cls,
            key: str,
            *,
            default: Optional[Any] = None,
            sep: str = ",",
            func: Optional[Callable[..., FuncResult]] = None
    ) -> List[Union[str, FuncResult]]:
        """
        Получить список значений из переменной окружения путем разбиения по разделителю

        :param key: имя переменной окружения
        :param default: значение по умолчанию
        :param sep: разделитель
        :param func: функция, которую нужно применить к КАЖДОМУ элементу результата
        :return: значение переменной окружения
        :raises NoEnvironmentException: если нет переменной окружения с именем `key`
        """
        value = cls.get_env_value(key, default=default)
        values = list(map(str.strip, value.split(sep)))

        if func is not None:
            values = list(map(func, values))

        return values
