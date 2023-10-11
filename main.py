# Library Includes
from Setup import Database, Models, Log
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import Status, WeatherStat, PowerStat

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine) 

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Start_Log()

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Stop_Log()

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)
PostOffice.include_router(PowerStat.PostOffice_PowerStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Get_Log(request)

	# Send Success
	return {"Service": "PostOffice", "Version": "02.00.00"}
 