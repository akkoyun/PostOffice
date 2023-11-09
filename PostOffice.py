# Library Includes
from Functions import Log
from Setup import Database, Models
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat, PowerStat
from datetime import datetime
from Setup.Config import APP_Settings

# Define FastAPI Object
PostOffice = FastAPI(version="02.01.00", title="PostOffice")

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

	# Message Status Code
	Message_Status_Code = status.HTTP_400_BAD_REQUEST

	# Message Content
	Message_Content = {"Event": status.HTTP_400_BAD_REQUEST, "Message": f"{exc}"}

	# Headers
	Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Send Response
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat, prefix="/WeatherStat", tags=["WeatherStat"], responses={404: {"Description": "Not found"}})
PostOffice.include_router(PowerStat.PostOffice_PowerStat, prefix="/PowerStat", tags=["PowerStat"], responses={404: {"Description": "Not found"}})

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
