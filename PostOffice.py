# Library Imports
from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Functions import Log, FastApi_Functions
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Tags
FastAPI_Tags = [
    {
        "name": "Root",
        "description": "This endpoint is the root of the PostOffice API.",
    }
]

# Define Lifespan
@asynccontextmanager
async def FastAPI_Lifespan(app: FastAPI):

	# Library Imports
	import time

	# Startup Functions
	Log.Terminal_Log("INFO", "Application is starting...")

	# Create Tables
	Database.Base.metadata.create_all(bind=Database.DB_Engine)

	# Run the application
	yield

	# Shutdown Functions
	Log.Terminal_Log("INFO", "Application is shutting down.")

	# Close Delays
	time.sleep(10)

# Define FastAPI Object
PostOffice = FastAPI(version="02.04.00", title="PostOffice", openapi_tags=FastAPI_Tags, lifespan=FastAPI_Lifespan)

# Define Middleware
PostOffice.add_middleware(FastApi_Functions.Pre_Request)

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Terminal_Log("ERROR", f"Undefinied Data : {request.body}")

	# Control for Null Body
	if exc.body is not None:

        # Add Stream to DataBase
#		Functions.Record_Stream(0, 0, request.client.host, request.headers['content-length'], exc.body, datetime.now())

		# Message Status Code
		Message_Status_Code = status.HTTP_400_BAD_REQUEST

		# Message Content
		Message_Content = {"Event": status.HTTP_400_BAD_REQUEST}

	# Null Body
	else:

		# Message Status Code
		Message_Status_Code = status.HTTP_406_NOT_ACCEPTABLE

		# Message Content
		Message_Content = {"Event": status.HTTP_406_NOT_ACCEPTABLE}

	# Send Response
	return JSONResponse(
		status_code=Message_Status_Code, 
		content=Message_Content
	)

# Main Root Get Method
@PostOffice.get("/", tags=["Root"], status_code=status.HTTP_200_OK)
def Main_Root(request: Request):

	# Library Imports
	from jinja2 import Environment, FileSystemLoader
	from pathlib import Path

	# Set up Jinja2 Environment
	Templates_Directory = Path("Templates")
	Jinja_ENV = Environment(loader=FileSystemLoader(Templates_Directory))

	# Define the error message
	Error_Message = f"Hata: İsteğiniz geçersiz. Yardım için destek ekibimize başvurun. [{request.client.host}]"

	# Load the HTML template
	Template = Jinja_ENV.get_template("HTML_Response.html")

	# Render the template with the footer message
	Rendered_HTML = Template.render(error_message=Error_Message)

	# Log Message
	Log.Terminal_Log("WARNING", f"New Root Request.")

	# Return the HTML content
	return HTMLResponse(content=Rendered_HTML)

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
async def Data_POST(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"Device ID : {Data.Info.ID}")
	Log.Terminal_Log("INFO", f"ICCID     : {Data.Device.IoT.ICCID}")
	Log.Terminal_Log("INFO", f"IMEI      : {Data.Device.IoT.IMEI}")







	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK}
	)