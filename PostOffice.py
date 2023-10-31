# Library Includes
from Functions import Log
from Setup import Database
from sqlalchemy import event

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat
from datetime import datetime

# After Table Create Event
def After_Create_Table(Target, Connection, **kw):

	# Get Tables
	tables = kw.get('tables', None)

	# Control Tables
	if tables:
        
		# Get Table Names
		table_names = [table.name for table in tables]
        
		# Log Message
		Log.Terminal_Log("INFO", f"Tables Created: {', '.join(table_names)}")

# Listeners
event.listen(Database.Base.metadata, 'after_create', After_Create_Table)

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine, checkfirst=True) 

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Shutdown {datetime.now()}")

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Terminal_Log("ERROR", f"New Undefinied Data Recieved from: {request.client.host}")

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"Event": status.HTTP_400_BAD_REQUEST, "Message": f"{exc}"},
	)

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")

	# Send Success
	return {
		"Service": "PostOffice", 
		"Version": "02.00.00", 
		"Status": {
			"PostOffice": 0, 
			"RAW_Handler": 0, 
			"WeatherStat_Handler": 0
		}
	}
