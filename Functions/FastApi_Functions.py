# Libraries
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from Functions import Log

class AddHeaderMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Define Response
        Response = await call_next(request)

        # Log Message
        Log.Terminal_Log("INFO", f"-----------------------------------------")

        # Return Response
        return Response