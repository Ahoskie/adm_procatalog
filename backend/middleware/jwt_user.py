import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.external import post_external_request


class AppendUserToRequest(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get('token')
        if not access_token:
            return JSONResponse(status_code=401, content={'detail': 'Token not found'})
        response = await call_next(request)
        return response
