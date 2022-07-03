from asyncio.windows_events import NULL
from typing import Optional
from fastapi import Body, Depends, FastAPI, APIRouter, Response, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .. import Models
from ..Database import DB_Engine, DB_Session, get_db

# Define Route Object
Device = APIRouter(
    prefix= "/Device",
    tags=['Device Operations']
)

# Define Schema
class Device_Post(BaseModel):
    Type: int
    ID: str
    Location: Optional[str]
    Owner: Optional[str]
    IP: Optional[str]




# Device End Point Default Request
@Device.get("/")
def Device_Root():
    return {"message": "Device End Point"}

# Device List
@Device.get("/List")
def Device_List(db: Session = Depends(get_db)):
    return {"Status": "OK"}

# Device Detail
@Device.get("/Detail/{id}")
def Device_Detail(id : int):
    return {"Device_List": id}

# Device Create
@Device.post("/Create", status_code=status.HTTP_201_CREATED)
def Device_Create(payload : Device_Post, response : Response):

    List_Dict = payload.dict()
    #raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Added")
    return {"Device_List": "Sample_Device_List"}
