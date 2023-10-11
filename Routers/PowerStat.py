# Library Includes
from Setup import Database, Models, Log, Schema
from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocket
import json

# Define FastAPI Object
PostOffice_PowerStat = APIRouter()

# IoT Post Service Health Check
@PostOffice_PowerStat.get("/PowerStat/")
async def get():
	return {"Event": status.HTTP_200_OK}