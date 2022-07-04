from fastapi import Depends, FastAPI
from Routers import Device

from sqlalchemy.orm import Session
from . import Models
from .Database import engine, SessionLocal

Models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    tags=['Root Operations']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root Message
@app.get("/")
def root():
    return {"message": "Hello PostOffice"}

# Database Path
@app.get("/DB")
def DB_Test(db: Session = Depends(get_db)):
    return {"message": "OK"}

# Device End Point Route
app.include_router(Device.Device)