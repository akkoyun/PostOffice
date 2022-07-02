from fastapi import FastAPI, APIRouter

# Define Route Object
Device = APIRouter(
    prefix= "/Device",
    tags=['Device Operations']
)

# Device End Point Default Request
@Device.get("/")
def Device_Root():
    return {"message": "Device End Point"}

# Device Create
@Device.post("/Create")
def root():
    return {"message": "Device Create"}