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
PostOffice_WeatherStat = APIRouter(default_redirect_slash=True)

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

	# Get Last Stream ID
	Last_Stream_ID = Handler.Get_Last_Stream_ID(ID)

	# Get Last Variables
	Last_AT = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4010)
	Last_AH = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4020)
	Last_AP = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4030)
	Last_UV = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4040)
	Last_ST10 = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4070)
	Last_ST30 = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4072)
	Last_ST60 = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4075)
	Last_ST90 = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4078)
	Last_WS = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4090)
	Last_WD = Handler.Get_WeatherStat_Data(Last_Stream_ID, 4100)









	# Set Max AT
	Max_AT = App_Schema.MaxAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set Min AT
	Min_AT = App_Schema.MinAT(Value=28.3232, Time="2022-07-19T08:28:32Z")

	# Set AT
	if Last_AT is not None:
		AT = App_Schema.AT(Value=Last_AT, Change=0, AT_FL=28.3232, AT_Dew=28.3232, Max_AT=Max_AT, Min_AT=Min_AT)

	# Set AH
	if Last_AH is not None:
		AH = App_Schema.AH(Value=Last_AH, Change=0)

	# Set AP
	if Last_AP is not None:
		AP = App_Schema.AP(Value=Last_AP, Change=0)

	# Set R
	R = App_Schema.R(R_1=28.3232, R_24=28.3232, R_48=2, R_168=28.3232)

	# Set Ws
	if Last_WS is not None and Last_WD is not None:
		W = App_Schema.W(WS=Last_WS, WD=Last_WD, Change=0)

	# Set UV
	if Last_UV is not None:
		UV = App_Schema.UV(Value=Last_UV, Change=0)

	# Set ST
	if Last_ST10 is not None:
		ST_10 = App_Schema.ST_10(Value=Last_ST10, Change=0)
	else:
		ST_10 = App_Schema.ST_10(Value=0, Change=0)
	if Last_ST30 is not None:
		ST_30 = App_Schema.ST_30(Value=Last_ST30, Change=0)
	else:
		ST_30 = App_Schema.ST_30(Value=0, Change=0)
	if Last_ST60 is not None:
		ST_60 = App_Schema.ST_60(Value=Last_ST60, Change=0)
	else:
		ST_60 = App_Schema.ST_60(Value=0, Change=0)
	if Last_ST90 is not None:
		ST_90 = App_Schema.ST_90(Value=Last_ST90, Change=0)
	else:
		ST_90 = App_Schema.ST_90(Value=0, Change=0)
	ST = App_Schema.ST(ST_10=ST_10, ST_30=ST_30, ST_60=ST_60, ST_90=ST_90)

	# Set Sun
	Sun = App_Schema.Sun(Sunrise="2022-07-19T08:28:32Z", Sunset="2022-07-19T08:28:32Z")

	# Set Model
	Response_Message = App_Schema.Model(Device=Device, AT=AT, AH=AH, AP=AP, R=R, W=W, UV=UV, ST=ST, Sun=Sun)

	# Set Response
	return Response_Message
	



