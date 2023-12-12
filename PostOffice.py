# Library Includes
from Functions import Log, Kafka, Handler, Functions
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
PostOffice = FastAPI(version="02.02.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")
	Log.Terminal_Log("DEBUG", f"*************************************************")

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Shutdown {datetime.now()}")

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Terminal_Log("ERROR", f"New Undefinied Data Recieved from: {request.client.host}")

	# Control for Null Body
	if exc.body is not None:

		# Define DB
		DB_Module = Database.SessionLocal()

		# Create New Stream
		New_Stream = Models.Stream(
			Device_ID = "0",
			ICCID = "1",
			Client_IP = request.client.host,
			Size = request.headers['content-length'],
			RAW_Data = exc.body,
			Device_Time = datetime.now(),
			Stream_Time = datetime.now()
		)

		# Add Stream to DataBase
		DB_Module.add(New_Stream)

		# Commit DataBase
		DB_Module.commit()

		# Refresh DataBase
		DB_Module.refresh(New_Stream)

		# Close Database
		DB_Module.close()

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
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")

	# Send Success
	return {
		"Service": PostOffice.openapi()["info"]["title"],
		"Version": PostOffice.openapi()["info"]["version"],
		"Status": {
			"Hardware_API": Functions.Get_Service_Status("PostOffice"), 
			"RAW Service": Functions.Get_Service_Status("Handler_RAW"),
			"Parameter Service": Functions.Get_Service_Status("Handler_Parameter"),
			"Payload Service": Functions.Get_Service_Status("Handler_Payload")
		}
	}

# IoT Post Method
@PostOffice.post("", status_code=status.HTTP_201_CREATED)
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
async def Data_POST(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")
	Log.Terminal_Log("INFO", f"Device ID: {Data.Info.ID}")

	# Get RAW Body
	RAW_Body = await request.body()

	# Clean RAW Body
	Clean_RAW_Body = RAW_Body.decode('utf-8').replace("\n", "").replace("\r", "").replace(" ", "")

    # Define DB
	DB = Database.SessionLocal()

	# Control Device Existance
	Query_Device = DB.query(Models.Device).filter(Models.Device.Device_ID == Data.Info.ID).first()

	# Control Device Existance
	if Query_Device is None:

		# Create New Device
		New_Device = Models.Device(
			Device_ID = Data.Info.ID,
			Status_ID = 1,
			Version_ID = 0,
			Model_ID = 0,
			IMEI = 0
		)

		# Add Device to DataBase
		DB.add(New_Device)

		# Commit DataBase
		DB.commit()

		# Refresh DataBase
		DB.refresh(New_Device)

		# Log Message
		Log.Terminal_Log("INFO", f"New Device.")

	# Device Found
	else:

		# Update Device Last_Connection
		Query_Device.Last_Connection = datetime.now()

		# Commit DataBase
		DB.commit()

		# Log Message
		Log.Terminal_Log("INFO", f"Device Found.")

	# Control for SIM
	SIM_Status = Functions.Update_SIM(Data.Device.IoT.ICCID)

	# Log Message
	if SIM_Status:
		Log.Terminal_Log("INFO", f"SIM: {Data.Device.IoT.ICCID} [NEW]")
	else:
		Log.Terminal_Log("INFO", f"SIM: {Data.Device.IoT.ICCID} [OLD]")

	# Create New Stream
	New_Stream = Models.Stream(
		Device_ID = Data.Info.ID,
		ICCID = Data.Device.IoT.ICCID,
		Client_IP = request.client.host,
		Size = request.headers['content-length'],
		RAW_Data = Clean_RAW_Body,
		Device_Time = Data.Info.TimeStamp,
		Stream_Time = datetime.now()
	)

	# Add Stream to DataBase
	DB.add(New_Stream)

	# Commit DataBase
	DB.commit()

	# Refresh DataBase
	DB.refresh(New_Stream)

	# Set headers
	Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8')),
        ("Stream_ID", bytes(str(New_Stream.Stream_ID), 'utf-8'))
	]

	# Log Message
	Log.Terminal_Log("INFO", f"Stream ID: {New_Stream.Stream_ID}")
	Log.Terminal_Log("INFO", f"-----------------------------------------------")

	# Send to Kafka Topic
	Kafka.Send_To_Topic("RAW", Data.json(), Header)

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK}
	)

# Record Info Get Method
@PostOffice.get("/Info", status_code=status.HTTP_200_OK)
@PostOffice.get("/Info/", status_code=status.HTTP_200_OK)
def Info(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Abstract Request: {request.client.host}")

	# Get Count
	Device_Count = Handler.Get_Count("Device")
	Data_Type_Count = Handler.Get_Count("Data_Type")
	Modem_Count = Handler.Get_Count("Modem")
	SIM_Count = Handler.Get_Count("SIM")
	Stream_Count = Handler.Get_Count("Stream")
	Parameter_Count = Handler.Get_Count("Parameter")
	Payload_Count = Handler.Get_Count("Payload")

	# Send Success
	return {
		"Device_Count": Device_Count,
		"Data_Type_Count": Data_Type_Count,
		"Modem_Count": Modem_Count,
		"SIM_Count": SIM_Count,
		"Stream_Count": Stream_Count,
		"Parameter_Count": Parameter_Count,
		"Payload_Count": Payload_Count
	}
