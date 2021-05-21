import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.external import post_external_request
from core.config import AUTH_IP


class AppendUserToRequest(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.headers.get('authorization')
        decoded_user = None
        if access_token:
            access_token = access_token[7:]
            response_data, status = post_external_request(AUTH_IP + '/api/users/verify-token/', token=access_token)
            if status != 200:
                return JSONResponse(status_code=401, content={'detail': 'Unable to authenticate user'})

            try:
                decoded_user = jwt.decode(access_token, algorithm='HS256', options={'verify_signature': False})
            except jwt.exceptions.InvalidTokenError or jwt.exceptions.DecodeError:
                return JSONResponse(status_code=401, content={'detail': 'Bad token format'})

        request.scope['user'] = decoded_user
        response = await call_next(request)
        return response
