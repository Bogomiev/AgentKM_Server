from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from src.auth.refresh import BearerTransportRefresh
from src.settings import ACCESS_TOKEN_EXPIRES, AUTH_SECRET_KEY, REFRESH_TOKEN_EXPIRES


bearer_transport = BearerTransport(tokenUrl="auth/login")
bearer_transport_refresh = BearerTransportRefresh(tokenUrl="auth/jwt/refresh")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AUTH_SECRET_KEY, lifetime_seconds=ACCESS_TOKEN_EXPIRES)


def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AUTH_SECRET_KEY, lifetime_seconds=REFRESH_TOKEN_EXPIRES)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
