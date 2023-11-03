# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema, App_Schema
from Functions import Log, Kafka, Handler
from Setup.Config import APP_Settings

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@PostOffice_WeatherStat.post("/", status_code=status.HTTP_201_CREATED)
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
@PostOffice_WeatherStat.get("/{ID}", response_model=App_Schema.Model, status_code=status.HTTP_200_OK)
def Mobile_App_Root(request: Request, ID: str) -> App_Schema.Model:

	# Get Device Last Connection Time
	Device_Last_Connection = Handler.Get_Device_Last_Connection(ID).strftime("%Y-%m-%d %H:%M:%S")

	# Set Device
	Device = App_Schema.Device(Device_ID=ID,LastUpdate=Device_Last_Connection)

	# Read Data
	AT_Data = Handler.Measurement(Handler.Read_Measurement(ID, "AT"))
#	AH_Data = Handler.Read_Measurement(ID, "AH")
#	AP_Data = Handler.Read_Measurement(ID, "AP")


	# Parse AT Data
	if AT_Data is not None:
		AT = App_Schema.AT(Value=AT_Data.Last_Value, Change=AT_Data.Change)

	# Parse AH Data
#	if AH_Data is not None:
#		AH = App_Schema.AH(Value=AH_Data.Last_Value, Change=AH_Data.Change)

	# Parse AP Data
#	if AP_Data is not None:
#		AP = App_Schema.AP(Value=AP_Data.Last_Value, Change=AP_Data.Change)




	# Set Model
#	Response_Message = App_Schema.Model(Device=Device, AT=AT, AH=AH, AP=AP)
	Response_Message = App_Schema.Model(Device=Device, AT=AT)

	# Set Response
	return Response_Message
	