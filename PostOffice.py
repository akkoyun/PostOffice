# Library Imports
from Setup import Database, Schema
from Setup.Config import APP_Settings
from Functions import Log, FastApi_Functions, Database_Functions, Kafka
from fastapi import FastAPI, Request, status, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Tags
FastAPI_Tags = [
    {
        "name": "Root",
        "description": "This endpoint is the root of the PostOffice API.",
    },
	{
		"name": "Hardware_Post",
		"description": "This endpoint is used to receive data from IoT devices."
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

	# Get Request Body
	Request_Body = ((await request.body()).decode("utf-8")).replace(" ", "").replace("\n", "").replace("\r", "")

	# Record Unknown Data
	Database_Functions.Record_Unknown_Data(request.client.host, Request_Body)

	# Control for Null Body
	if exc.body is not None:

		# Message Status Code
		Message_Status_Code = status.HTTP_400_BAD_REQUEST

		# Log Message
		Log.Terminal_Log("ERROR", f"Error : {exc.errors()}")

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
	Error_Message = f"Hata : İsteğiniz geçersiz. Yardım için destek ekibimize başvurun. [{request.client.host}]"

	# Load the HTML template
	Template = Jinja_ENV.get_template("HTML_Response.html")

	# Render the template with the footer message
	Rendered_HTML = Template.render(error_message=Error_Message)

	# Log Message
	Log.Terminal_Log("WARNING", f"New Root Request.")

	# Return the HTML content
	return HTMLResponse(content=Rendered_HTML)

# IoT Post Method
@PostOffice.post("/", tags=["Hardware_Post"], status_code=status.HTTP_201_CREATED)
async def Data_POST(request: Request, Data: Schema.Data_Pack, Send_Kafka: BackgroundTasks):

	# Log Message
	Log.Terminal_Log("INFO", f"Device ID : {Data.Info.ID}")
	Log.Terminal_Log("INFO", f"ICCID     : {Data.Device.IoT.ICCID}")
	Log.Terminal_Log("INFO", f"IMEI      : {Data.Device.IoT.IMEI}")

	# Get Request Body
	Request_Body = ((await request.body()).decode("utf-8")).replace(" ", "").replace("\n", "").replace("\r", "")

	# Set headers
	Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8'))
	] 

	# Produce Message
	Send_Kafka.add_task(Kafka.Send_To_Topic, APP_Settings.KAFKA_RAW_TOPIC, Request_Body, Header, 0)

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK}
	)