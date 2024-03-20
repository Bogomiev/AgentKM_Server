from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from settings import SECRET_KEY

session_middleware_params = dict(
    middleware_class=SessionMiddleware,
    secret_key=SECRET_KEY
)

cors_middleware_params = dict(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MIDDLEWARES = [
    session_middleware_params,
    cors_middleware_params
]


def add_all_middlewares(
        app: FastAPI,
) -> None:
    """Добавить все middlewares в приложение"""
    for middleware_params in MIDDLEWARES:
        app.add_middleware(**middleware_params)
