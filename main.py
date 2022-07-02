from fastapi import FastAPI
from Routers import Device

app = FastAPI(
    tags=['Root Operations']
)

# Root Message
@app.get("/")
def root():
    return {"message": "Hello PostOffice"}

# Device End Point Route
app.include_router(Device.Device)