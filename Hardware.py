# Library Includes
from Functions import Log, Kafka, Functions
from Setup import Schema
from Setup.Config import APP_Settings
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
Hardware_API = FastAPI(version="01.00.00", title="Hardware API")

# API Boot Sequence
@Hardware_API.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"Hardware API Started {datetime.now()}")
	Log.Terminal_Log("DEBUG", f"*************************************************")

# API ShutDown Sequence
@Hardware_API.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"Hardware API Shutdown {datetime.now()}")

# Schema Error Handler
@Hardware_API.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Terminal_Log("ERROR", f"New Undefinied Data Recieved from: {request.client.host}")

	# Control for Null Body
	if exc.body is not None:

        # Add Stream to DataBase
		Functions.Record_Stream(0, 0, request.client.host, request.headers['content-length'], exc.body, datetime.now())

		# Message Status Code
		Message_Status_Code = status.HTTP_400_BAD_REQUEST

		# Message Content
		Message_Content = {"Event": status.HTTP_400_BAD_REQUEST, "Message": f"{exc}"}

		# Headers
		Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Null Body
	else:

		# Message Status Code
		Message_Status_Code = status.HTTP_406_NOT_ACCEPTABLE

		# Message Content
		Message_Content = {"Event": status.HTTP_406_NOT_ACCEPTABLE, "Message": "Null Body"}

		# Headers
		Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Send Response
	return JSONResponse(
		status_code=Message_Status_Code, 
		content=Message_Content, 
		headers=Message_Headers
	)

# IoT Post Method
@Hardware_API.post("", status_code=status.HTTP_200_OK)
async def Hardware_API(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {Data.Info.ID} / {request.client.host}")

	# Get Request Body
	Request_Body = ((await request.body()).decode("utf-8")).replace(" ", "").replace("\n", "").replace("\r", "")

	# Set headers
	Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8')),
		("Body", bytes(Request_Body, 'utf-8'))
	]

	# Send to Kafka Topic
	Kafka.Send_To_Topic("Hardware", Data.json(), Header)

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK}
	)
