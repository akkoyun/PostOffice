# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema, Database, App_Schema
from Functions import Log, Kafka, Handler
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

	# Get Device Last Connection Time
	Device_Last_Connection = Handler.Get_Device_Last_Connection(ID)

	# Set Device
	Device = App_Schema.Device(LastUpdate=Device_Last_Connection)








	# Set Max AT
	Max_AT = App_Schema.MaxAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set Min AT
	Min_AT = App_Schema.MinAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set AT
	AT = App_Schema.AT(Value=28.3232, Change=0, AT_FL=28.3232, AT_Dew=28.3232, Max_AT=Max_AT, Min_AT=Min_AT)

	# Set AH
	AH = App_Schema.AH(Value=28.3232, Change=0)

	# Set AP
	AP = App_Schema.AP(Value=28.3232, Change=0)

	# Set R
	R = App_Schema.R(R_1=28.3232, R_24=28.3232, R_48=2, R_168=28.3232)

	# Set W
	W = App_Schema.W(WS=28.3232, WD=28.3232, Change=0)

	# Set UV
	UV = App_Schema.UV(Value=28.3232, Change=0)

	# Set ST
	ST_10 = App_Schema.ST_10(Value=28.3232, Change=0)
	ST_30 = App_Schema.ST_30(Value=28.3232, Change=0)
	ST_60 = App_Schema.ST_60(Value=28.3232, Change=0)
	ST_90 = App_Schema.ST_90(Value=28.3232, Change=0)
	ST = App_Schema.ST(ST_10=ST_10, ST_30=ST_30, ST_60=ST_60, ST_90=ST_90)

	# Set Sun
	Sun = App_Schema.Sun(Sunrise="2022-07-19T08:28:32Z", Sunset="2022-07-19T08:28:32Z")

	# Set Model
	Response_Message = App_Schema.Model(Device=Device, AT=AT, AH=AH, AP=AP, R=R, W=W, UV=UV, ST=ST, Sun=Sun)

	# Set Response
	return Response_Message
	



