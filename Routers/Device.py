from typing import Optional
from fastapi import Body, FastAPI, APIRouter, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# Define Route Object
Device = APIRouter(
    prefix= "/Device",
    tags=['Device Operations']
)

# Define Schema
class Device_Post(BaseModel):
    Type: int = 101
    ID: str
    Location: Optional[str] = "STF HQ"
    Owner: Optional[str] = "STF"
    IP: Optional[str] = "0.0.0.0"

try:
    conn = psycopg2.connect(host='localhost', database='postgre', user='postgre', password='00204063f4b4!N', cursor_factory=RealDictCursor )
    cursor = conn.cursor()
except Exception as error:
    print("Fail")




Sample_Device_List = [
    {"Type" :101, "ID" : "00112233445566", "Location" : "Konya", "Owner" : "STF", "IP" : "1.1.1.1"},
    {"Type" :102, "ID" : "00112233445566", "Location" : "Sarayonu", "Owner" : "STF", "IP" : "2.2.2.2"}
    ]






# Device End Point Default Request
@Device.get("/")
def Device_Root():
    return {"message": "Device End Point"}

# Device List
@Device.get("/List")
def Device_List():
    cursor.execute(""" SELECT * FROM Devices """)
    post = cursor.fetchall()
    return {"Device_List": post}

# Device Detail
@Device.get("/Detail/{id}")
def Device_Detail(id : int):
    return {"Device_List": id}

# Device Create
@Device.post("/Create")
def Device_Create(payload : Device_Post, response : Response):
    List_Dict = payload.dict()
    Sample_Device_List.append(List_Dict)

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Added")

    return {"Device_List": Sample_Device_List}