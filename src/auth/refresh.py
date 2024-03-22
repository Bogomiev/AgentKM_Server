from fastapi.openapi.models import Response
from fastapi_users import models
from fastapi_users.authentication import BearerTransport, AuthenticationBackend, Transport, Strategy
from fastapi_users.types import DependencyCallable
from pydantic import BaseModel
from starlette.responses import JSONResponse


class BearerResponseRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class BearerTransportRefresh(BearerTransport):
    async def get_login_response(self, token: str, refresh_token: str) -> JSONResponse:
        bearer_response = BearerResponseRefresh(
            access_token=token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        return JSONResponse(bearer_response.dict())


class AuthenticationBackendRefresh(AuthenticationBackend):
    def __init__(
        self,
        name: str,
        transport: Transport,
        get_strategy: DependencyCallable[Strategy[models.UP, models.ID]],
        get_refresh_strategy: DependencyCallable[Strategy[models.UP, models.ID]]
    ):
        self.name = name
        self.transport = transport
        self.get_strategy = get_strategy
        self.get_refresh_strategy = get_refresh_strategy

    async def login(
        self,
        strategy: Strategy[models.UP, models.ID],
        user: models.UP,
    ) -> Response:
        token = await strategy.write_token(user)
        refresh_strategy = self.get_refresh_strategy()
        refresh_token = await refresh_strategy.write_token(user)
        return await self.transport.get_login_response(token=token, refresh_token=refresh_token)

