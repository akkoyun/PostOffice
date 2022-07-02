from fastapi import FastAPI
from Routers import Device

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello PostOffice"}

# Device End Point Route
app.include_router(Device.Device)