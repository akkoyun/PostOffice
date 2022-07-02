from fastapi import FastAPI
from .Routers import Device

API = FastAPI()

@API.get("/")
def root():
    return {"message": "Hello PostOffice"}

# Device End Point Route
API.include_router(Device.Device)