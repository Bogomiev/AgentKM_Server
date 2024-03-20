from fastapi_users.authentication import BearerTransport
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


