# Library Includes
from Functions import Log, Functions
from Setup.Config import APP_Settings
from Setup import Schema
from fastapi import FastAPI, Request, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
Hardware = FastAPI(version="01.00.00", title="Hardware")

# API Middleware Sequence
@Hardware.middleware("http")
async def MiddleWare(request: Request, call_next):

    # Log Message
    Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")
    Log.Terminal_Log("INFO", f"****************************************")

    # Set Response
    Response = await call_next(request)
	
    # End Function
    return Response

# Schema Error Handler
@Hardware.exception_handler(RequestValidationError)
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

# IoT Get Method
@Hardware.get("/", status_code=status.HTTP_200_OK, response_model=Schema.Hardware_API_Response_Model)
async def Root(request: Request, x_real_ip: str = Header(None)):

	# Define Status Code
	HTTP_Status_Code = status.HTTP_202_ACCEPTED

	# Set Response Event
	Response_Event = 210

	# Create Response Content
	Response_Pack = Schema.Hardware_API_Response_Model(Event=Response_Event)

	# Send Success
	return Response_Pack, HTTP_Status_Code
