import enum
from typing import List, Union, Type

from pydantic import Field

from src.base.result_codes import ResultCodes


def get_description_of_enum(clazz: Type[enum.Enum]) -> str:
    """Получить HTML описание enum класса на основе его docstring и значений"""
    items = map(lambda x: "{} - {}".format(x.name, x.value), clazz)
    items = map(lambda x: "<li>{}</li>".format(x), items)
    items = "<ul>{}</ul>".format("".join(items))

    return "\n".join((
        clazz.__doc__.strip().splitlines()[0],
        "",
        items
    ))


_description_of_result_codes = get_description_of_enum(ResultCodes)


class ResponseData:
    """
    Базовая модель данных для ответа клиенту api
    """
    result_code: ResultCodes = Field(..., description=_description_of_result_codes)
    messages: List[str] = Field(default_factory=list, description="Сообщения")
    data: Union[dict, List] = Field(default_factory=dict, description="Основные данные")


class SuccessResponseData(ResponseData):
    """
    Модель данных для успешного ответа клиенту api
    """
    result_code: ResultCodes = Field(ResultCodes.SUCCESS,
                                     description=_description_of_result_codes)
    messages: List[str] = Field(["ok"], description="Сообщения")


class ErrorResponseData(ResponseData):
    """
    Модель данных для ответа об ошибке клиенту api
    """
    result_code: ResultCodes = Field(ResultCodes.ERROR,
                                     description=_description_of_result_codes)
    messages: List[str] = Field(["error message"], description="Сообщения")
