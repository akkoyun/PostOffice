from fastapi import Body, FastAPI, APIRouter

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
def Device_Create(payload : dict = Body(...)):
    return {"message": f"request {payload['Device']['ID']}"}