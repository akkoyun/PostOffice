# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema
from Functions import Log, Kafka
from Setup.Config import APP_Settings

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")

	# Set headers
	RAW_Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8')),
	]
	
	# Send to Kafka Topic
	Kafka.Send_To_Topic("RAW", Data.json(), RAW_Header)

	# Log Message
	Log.Terminal_Log("INFO", f"****************************************")

	# Message Status Code
	Message_Status_Code = status.HTTP_200_OK

	# Message Content
	Message_Content = {"Event": status.HTTP_200_OK}

	# Headers
	Server_Name = APP_Settings.SERVER_NAME
	Message_Headers = {"server": Server_Name}

	# Send Response
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)


