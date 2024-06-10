# Libraries
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from Functions import Log

class Pre_Request(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Log Message
        Log.Terminal_Log("INFO", f"-----------------------------------------")
        Log.Terminal_Log("INFO", f"Client IP : {request.client.host}")

        # Define Response
        Response = await call_next(request)

        # Return Response
        return Response