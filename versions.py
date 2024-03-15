from typing import NamedTuple, Iterable, Union

from fastapi import APIRouter, FastAPI

import middlewares
from utils.url import url_concat


class FirstVersionAPIRouterItem(NamedTuple):
    """Элемент первой версии (без префикса) роутера REST API"""
    router: APIRouter
    settings: dict
    prefix: str = "/"
    version: str = "1.0"

    _docs_url = "/docs"

    @staticmethod
    def get_api_prefix() -> str:
        """Получить полный префикс версионированного роутера"""
        return "/"

    def get_docs_link(self) -> str:
        """Получить HTML ссылку на документацию Swagger"""
        href = url_concat(self.get_api_prefix(), self._docs_url)
        return f'<a class="link" href="{href}">' \
               f'<span class="url">Версия {self.version} (без префикса)</span>' \
               f'</a>'


class VersionedAPIRouterItem(NamedTuple):
    """Элемент версионированного роутера REST API"""
    router: APIRouter
    settings: dict
    prefix: str
    version: str

    _docs_url = "/docs"

    def get_api_prefix(self) -> str:
        """Получить полный префикс версионированного роутера"""
        return url_concat(self.prefix, f"v{self.version}")

    def get_docs_link(self) -> str:
        """Получить HTML ссылку на документацию Swagger"""
        href = url_concat(self.get_api_prefix(), self._docs_url)
        return f'<a class="link" href="{href}">' \
               f'<span class="url">Версия {self.version}</span>' \
               f'</a>'


def add_api_sub_app(
        base_app: FastAPI,
        router: APIRouter,
        settings: dict,
        description: str,
        api_prefix: str,
        version: str
) -> None:
    """
    Подключить router под определенной версией

    :param base_app: базовое приложение FastAPI
    :param router: добавляемый router API
    :param settings: настройки приложения FastAPI
    :param description: описание
    :param api_prefix: API префикс (включает в себя версию)
    :param version: версия
    :return:
    """
    # создаю новое sub приложение
    sub_app = FastAPI(
        **settings,
        description=description,
        version=version
    )

    # подключение middlewares
    middlewares.add_all_middlewares(sub_app)

    # подключаю роутер к sub приложению
    sub_app.include_router(router)

    # монтирую sub приложение к основному приложению
    base_app.mount(
        api_prefix,
        sub_app
    )


def mount_api_router_items(
        base_app: FastAPI,
        description: str,
        api_router_items: Iterable[Union[FirstVersionAPIRouterItem, VersionedAPIRouterItem]]
) -> None:
    """Подключить все роутеры REST API"""
    for item in api_router_items:
        if type(item) is FirstVersionAPIRouterItem:
            base_app.include_router(item.router)
        else:
            add_api_sub_app(
                base_app=base_app,
                router=item.router,
                settings=item.settings,
                description=description,
                api_prefix=item.get_api_prefix(),
                version=item.version
            )
