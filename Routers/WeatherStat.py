# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema, Database, App_Schema
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
	Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Send Response
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)

# IoT Get Method
@PostOffice_WeatherStat.get("/WeatherStat/{ID}", response_model=App_Schema.Model, status_code=status.HTTP_200_OK)
def Mobile_App_Root(request: Request, ID: str) -> App_Schema.Model:

	# Set Device
	Device = App_Schema.Device(LastUpdate="2022-07-19T08:28:32Z")

	# Set Max AT
	Max_AT = App_Schema.MaxAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set Min AT
	Min_AT = App_Schema.MinAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set AT
	AT = App_Schema.AT(Value=28.3232, Change=0, AT_FL=28.3232, AT_Dew=28.3232, Max_AT=Max_AT, Min_AT=Min_AT)

	# Set Model
	Response_Message = App_Schema.Model(Device=Device, AT=AT)

	# Set Response
	return Response_Message
	



