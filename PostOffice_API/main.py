from fastapi import FastAPI, status
from . import DataBase_Models
from .Database import DB_Engine, Get_DataBase
from .Routers import Post
from .Config import Settings

# Control for Table
DataBase_Models.Base.metadata.create_all(bind=DB_Engine)

# Declare Object
PostOffice = FastAPI(title="STF PostOffice V1")

# Route Request
PostOffice.include_router(Post.router)

# Default Request
@PostOffice.get("/", status_code=status.HTTP_202_ACCEPTED)
def root():
	return {"PostOffice API": "v01.00.01"}

