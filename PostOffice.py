# Library Includes
from Functions import Log, Kafka, Handler, Functions
import http.client
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
from fastapi import FastAPI, Request, status, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import pytz
import hashlib
import json

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
PostOffice = FastAPI(version="02.03.00", title="PostOffice")

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
	Log.Terminal_Log("INFO", f"New Data Recieved from: {Data.Info.ID} / {request.client.host}")

	# Get Request Body
	Request_Body = ((await request.body()).decode("utf-8")).replace(" ", "").replace("\n", "").replace("\r", "")

	# Set headers
	Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8')),
		("Body", bytes(Request_Body, 'utf-8'))
	]

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

# Firmware Get Method
@PostOffice.get("/Firmware/{Version_ID}", status_code=status.HTTP_200_OK)
@PostOffice.get("/Firmware/{Version_ID}/", status_code=status.HTTP_200_OK)
def Firmware(request: Request, Version_ID: int):

	# Set File Path
	Firmware_File_Path = f"/root/PostOffice/Docs/Firmware/"

    # Define DB
	with Database.DB_Session_Scope() as DB_Firmware:

		# Query Firmware
		Firmware = DB_Firmware.query(Models.Firmware).filter(Models.Firmware.Version_ID == Version_ID).first()

		# Control for Firmware
		if Firmware is None:

			# Log Message
			Log.Terminal_Log("ERROR", f"New Firmware Request: {request.client.host} [{Version_ID} / Not Found]")

            # Send Error
			return JSONResponse(
				status_code=status.HTTP_404_NOT_FOUND, 
				content={"Event": status.HTTP_404_NOT_FOUND, "Message": "Version ID Not Found"}
			)
        
		# Firmware Found
		else:

			# Log Message
			Log.Terminal_Log("INFO", f"New Firmware Request: {request.client.host} [{Version_ID} / Ready]")

			# Set File Path
			Firmware_File_Path += f"{Firmware.File_Name}"

			with open(Firmware_File_Path, "rb") as file:
				file_content = file.read()
				etag = hashlib.md5(file_content).hexdigest()
			
			headers = {"Etag": etag}

			# Return File
			return FileResponse(
                path=Firmware_File_Path, 
                filename=Firmware.File_Name, 
                media_type='application/octet-stream',
				headers=headers
            )

# Send Command Method
@PostOffice.get("/Device/{Device_ID}/Firmware/Download/{File_ID}", status_code=status.HTTP_200_OK)
@PostOffice.get("/Device/{Device_ID}/Firmware/Download/{File_ID}/", status_code=status.HTTP_200_OK)
def Firmware_Download(Device_ID: str, File_ID: int):

	# Get Last IP
	Last_IP = Handler.Get_Device_Last_IP(Device_ID)

	# Log Message
	Log.Terminal_Log("INFO", f"New Firmware FTP Download Request: [{Device_ID} - {Last_IP}] / {File_ID}.hex")

	# Connect to Device
	Connection = http.client.HTTPConnection(Last_IP)

	# Set Payload JSON
	Payload = f"{{\"Request\":{{\"Event\":901,\"FW_ID\":{File_ID}}}}}"

	# Set Headers
	Headers = {}

	# Send Request
	Connection.request("POST", "/", Payload, Headers)

	# Get Response
	Response = Connection.getresponse()

	# Read Data
	Data = Response.read()

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK, "Message": Data.decode("utf-8")}
	)

# Send Command Method
@PostOffice.get("/Device/{Device_ID}/Firmware/Burn", status_code=status.HTTP_200_OK)
@PostOffice.get("/Device/{Device_ID}/Firmware/Burn/", status_code=status.HTTP_200_OK)
def Firmware_Burn(Device_ID: str):

	# Get Last IP
	Last_IP = Handler.Get_Device_Last_IP(Device_ID)

	# Log Message
	Log.Terminal_Log("INFO", f"New Firmware Burn Request: [{Device_ID} - {Last_IP}]")

	# Connect to Device
	Connection = http.client.HTTPConnection(Last_IP)

	# Set Payload JSON
	Payload = f"{{\"Request\":{{\"Event\":950}}}}"

	# Set Headers
	Headers = {}

	# Send Request
	Connection.request("POST", "/", Payload, Headers)

	# Get Response
	Response = Connection.getresponse()

	# Read Data
	Data = Response.read()

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content={"Event": status.HTTP_200_OK, "Message": Data.decode("utf-8")}
	)

# Send Command Method
@PostOffice.post("/Device/{Device_ID}", status_code=status.HTTP_200_OK)
async def Command(request: Request, Device_ID: str):

	# Get Last IP
	Last_IP = Handler.Get_Device_Last_IP(Device_ID)

	# Parse Payload
	Payload = ((await request.body()).decode("utf-8"))

	# Log Message
	Log.Terminal_Log("INFO", f"Command Sended to Device: [{Device_ID} - {Last_IP}] / [{Payload}]")

	# Connect to Device
	Connection = http.client.HTTPConnection(Last_IP)

	# Set Headers
	Headers = {}

	# Send Request
	Connection.request("POST", "/", Payload, Headers)

	# Get Response
	Response = Connection.getresponse()

	# Read Data
	Data = Response.read()

	# Send Response
	return JSONResponse(
		status_code=Response.status, 
		content=json.loads(Data)
	)

# Send Command Method
@PostOffice.post("/Old_Device/{Device_IP}", status_code=status.HTTP_200_OK)
async def Command_Old(request: Request, Device_IP: str):

	# Connect to Device
	Connection = http.client.HTTPConnection(Device_IP)

	# Set Headers
	Headers = {}

	# Get Request Body
	Request_Body = ((await request.body()).decode("utf-8"))

	# Log Message
	Log.Terminal_Log("INFO", f"Body : [{Request_Body}]")

	# Send Request
	Connection.request("POST", "/", Request_Body, Headers)

	# Get Response
	Response = Connection.getresponse()

	# Read Data
	Data = Response.read()

	# Log Message
	Log.Terminal_Log("INFO", f"Command Sended : [{Data}]")

	# Send Response
	return JSONResponse(
		status_code=status.HTTP_200_OK, 
		content=Data.decode("utf-8")
	)

@PostOffice.websocket("/WS/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):

	await websocket.accept()

	Log.Terminal_Log("INFO", f"New WebSocket Connection: Client ID [{client_id}] has connected.")
    
	while True:

		data = await websocket.receive_text()

		Log.Terminal_Log("INFO", f"New WebSocket Data: [{client_id}] - [{data}]")

		await websocket.send_json({"Event": 200})
