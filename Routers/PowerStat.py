# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema, App_Schema
from Functions import Log, Kafka, Handler
from Setup.Config import APP_Settings
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
PostOffice_PowerStat = APIRouter()

# IoT Post Method
@PostOffice_PowerStat.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@PostOffice_PowerStat.post("/", status_code=status.HTTP_201_CREATED)
async def PowerStat_POST(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")










	# Message Status Code
	Message_Status_Code = status.HTTP_200_OK

	# Message Content
	Message_Content = {"Event": status.HTTP_200_OK}

	# Headers
	Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Send Response
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)
