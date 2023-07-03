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

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Unknown_Log(request)

	# Create Add Record Command
	New_Buffer = Models.Wrong_Data_Buffer(
		Buffer_Client_IP = request.client.host,
		Buffer_Data = str(exc.errors()))

	# Define DB
	DB_Buffer = Database.SessionLocal()

	# Add and Refresh DataBase
	DB_Buffer.add(New_Buffer)
	DB_Buffer.commit()
	DB_Buffer.refresh(New_Buffer)

	# Close Database
	DB_Buffer.close()

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content=exc.errors()
	)

# Include Routers
PostOffice.include_router(Status.PostOffice_Status)
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)
PostOffice.include_router(PowerStat.PostOffice_PowerStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Get_Log(request)

	# Send Success
	return {"Service": "PostOffice", "Version": "02.00.00"}
 