from fastapi import Body, FastAPI, APIRouter
from pydantic import BaseModel

# Define Route Object
Device = APIRouter(
    prefix= "/Device",
    tags=['Device Operations']
)

# Define Schema
class Device_Post(BaseModel):
    Type: int
    ID: str
    Location: str
    Owner: str
    IP: str

# Device End Point Default Request
@Device.get("/")
def Device_Root():
    return {"message": "Device End Point"}

# Device Create
@Device.post("/Create")
def Device_Create(payload : Device_Post):
    return {"Device_ID": payload.ID}