# Library Includes
from Functions import Log
from Setup import Database, Models
from fastapi import FastAPI, Request, status, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat
from datetime import datetime

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")
	Log.Terminal_Log("DEBUG", f"*************************************************")

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

    # Define DB
	DB_Module = Database.SessionLocal()

	# Create New Stream
	New_Stream = Models.Stream(
		Device_ID = "0",
		ICCID = "1",
		Client_IP = request.client.host,
		Size = request.headers['content-length'],
		RAW_Data = exc.body,
		Device_Time = datetime.now(),
		Stream_Time = datetime.now()
	)

	# Add Stream to DataBase
	DB_Module.add(New_Stream)

	# Commit DataBase
	DB_Module.commit()

	# Refresh DataBase
	DB_Module.refresh(New_Stream)

    # Close Database
	DB_Module.close()

	content = {"message": "Hello World"}
	headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
	return JSONResponse(content=content, headers=headers)

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		headers={"Server": "PostOffice"},
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
