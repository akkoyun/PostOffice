from fastapi import FastAPI, APIRouter

# Define Route Object
Device = APIRouter(
    prefix= "/Device",
    tags=['Device Operations']
)

# Device End Point Default Request
@Device.get("/")
def root():
    return {"message": "Device End Point"}