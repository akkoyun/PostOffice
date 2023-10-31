# Library Includes
from Functions import Log
from Setup import Database, Models
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat
from datetime import datetime
from sqlalchemy import MetaData, inspect
from Setup import Data_Update

# Update Database Inspector
DB_Inspector = inspect(Database.DB_Engine)

# Get Table Names
DB_Old_Table_Names = DB_Inspector.get_table_names()

# Create DB Models
Models.Base.metadata.create_all(bind=Database.DB_Engine, checkfirst=True)

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")
	Log.Terminal_Log("DEBUG", f"*************************************************")

	# Update Database Inspector
	DB_Inspector = inspect(Database.DB_Engine)

	# Get Table Names
	DB_New_Table_Names = DB_Inspector.get_table_names()

	# Set New Tables
	DB_New_Table_List = list(set(DB_New_Table_Names) - set(DB_Old_Table_Names))

	# Order Tables
	if 'Modem' in DB_New_Table_List:
		DB_New_Table_List.remove('Modem')
		DB_New_Table_List.append('Modem')
	if 'SIM' in DB_New_Table_List:
		DB_New_Table_List.remove('SIM')
		DB_New_Table_List.append('SIM')
	if 'Data_Segment' in DB_New_Table_List:
		DB_New_Table_List.remove('Data_Segment')
		DB_New_Table_List.append('Data_Segment')
	if 'Data_Type' in DB_New_Table_List:
		DB_New_Table_List.remove('Data_Type')
		DB_New_Table_List.append('Data_Type')
	if 'Parameter' in DB_New_Table_List:
		DB_New_Table_List.remove('Parameter')
		DB_New_Table_List.append('Parameter')
	if 'WeatherStat' in DB_New_Table_List:
		DB_New_Table_List.remove('WeatherStat')
		DB_New_Table_List.append('WeatherStat')
	if 'PowerStat' in DB_New_Table_List:
		DB_New_Table_List.remove('PowerStat')
		DB_New_Table_List.append('PowerStat')
	if 'Device' in DB_New_Table_List:
		DB_New_Table_List.remove('Device')
		DB_New_Table_List.append('Device')

	# Check For Default Records
	for Table in DB_New_Table_List:
		
		# Check SIM Table
		if Table == "GSM_Operator": 
			
			# Define DB
			DB_Module = Database.SessionLocal()

			# Import GSM Operator
			Data_Update.Import_GSM_Operator(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()
		
		# Check for Data_Segment Table
		elif Table == "Data_Segment":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Data_Segment
			Data_Update.Import_Data_Segment(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Status Table
		elif Table == "Status":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Status
			Data_Update.Import_Status(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Version Table
		elif Table == "Version":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Version
			Data_Update.Import_Version(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Model Table
		elif Table == "Model":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Model
			Data_Update.Import_Model(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Manufacturer Table
		elif Table == "Manufacturer":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Manufacturer
			Data_Update.Import_Manufacturer(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Modem Table
		elif Table == "Modem":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Modem
			Data_Update.Import_Modem(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Data_Type Table
		elif Table == "Data_Type":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Data_Type
			Data_Update.Import_Data_Type(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for SIM Table
		elif Table == "SIM":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import SIM
			Data_Update.Import_SIM(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

		# Check for Device Table
		elif Table == "Device":

			# Define DB
			DB_Module = Database.SessionLocal()

			# Import Device
			Data_Update.Import_Device(DB_Module)

			# Define DB
			DB_Module = Database.SessionLocal()

	# Log Message
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

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"Event": status.HTTP_400_BAD_REQUEST, "Message": f"{exc}"},
	)

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")

	# Send Success
	return {
		"Service": "PostOffice", 
		"Version": "02.00.00", 
		"Status": {
			"PostOffice": 0, 
			"RAW_Handler": 0, 
			"WeatherStat_Handler": 0
		}
	}
