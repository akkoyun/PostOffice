# Library Includes
from Setup import Database, Models, Log, Kafka
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat, PowerStat
from datetime import datetime
from Setup.Default_Value_Update import Value_Update

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine, checkfirst=True) 

# Database Default Values
Value_Update()

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")

	# Log to Queue
	Kafka.Send_To_Log_Topic("SYSTEM", f"PostOffice API Started {datetime.now()}")

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Shutdown {datetime.now()}")

	# Log to Queue
	Kafka.Send_To_Log_Topic("SYSTEM", f"PostOffice API Stopped {datetime.now()}")

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Terminal_Log("ERROR", f"New Undefinied Data Recieved from: {request.client.host}")

	# Log to Queue
	Kafka.Send_To_Log_Topic("ERROR", f"Wrong Pack: {request.client.host}")

	# Create Add Record Command
	Undefinied_RAW_Data = Models.RAW_Data(
		RAW_Data_IP = request.client.host,
		RAW_Data = exc.body,
		RAW_Data_Valid = False
	)

	# Define DB
	DB_Undefinied_RAW_Data = Database.SessionLocal()

	# Add Record to DataBase
	try:

		# Add Record to DataBase
		DB_Undefinied_RAW_Data.add(Undefinied_RAW_Data)

		# Database Flush
		DB_Undefinied_RAW_Data.flush()

		# Commit DataBase
		DB_Undefinied_RAW_Data.commit()

		# Log Message
		Log.Terminal_Log("INFO", "Data Recorded to RAW Table")

	except Exception as e:

		# Log Message
		Log.Terminal_Log("ERROR", f"An error occurred while adding RAW_Data: {e}")

		# Rollback DataBase
		DB_Undefinied_RAW_Data.rollback()

	finally:

		# Close Database
		DB_Undefinied_RAW_Data.close()

	# Send Message to Queue
	Kafka.Kafka_Producer.send(topic='UNDEFINED', value=exc.body).add_callback(Kafka.Send_Success).add_errback(Kafka.Send_Error)

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
 		content={"Event": status.HTTP_400_BAD_REQUEST, "Message": f"{exc}"},
	)

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)
PostOffice.include_router(PowerStat.PostOffice_PowerStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")

	# Log to Queue
	Kafka.Send_To_Log_Topic("INFO", f"New Get Request: {request.client.host}")

	# Define DB
	DB_Module = Database.SessionLocal()

	# Service Query
	Service_PostOffice_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("PostOffice")).order_by(Models.Service_LOG.Service_Update_Time.desc()).first()
	Service_RAW_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_RAW")).order_by(Models.Service_LOG.Service_Update_Time.desc()).first()
	Service_Info_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_Info")).order_by(Models.Service_LOG.Service_Update_Time.desc()).first()
	Service_Power_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_Power")).order_by(Models.Service_LOG.Service_Update_Time.desc()).first()
	Service_IoT_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_IoT")).order_by(Models.Service_LOG.Service_Update_Time.desc()).first()

	# Get Service Status
	PostOffice_Status = Service_PostOffice_Status.Service_Status
	RAW_Status = Service_RAW_Status.Service_Status
	Info_Status = Service_Info_Status.Service_Status
	Power_Status = Service_Power_Status.Service_Status
	IoT_Status = Service_IoT_Status.Service_Status
	
	# Close Database
	DB_Module.close()

	# Send Success
	return {
		"Service": "PostOffice", 
		"Version": "02.00.00", 
		"Status": {
			"PostOffice": PostOffice_Status, 
			"RAW_Handler": RAW_Status, 
			"Info_Handler": Info_Status, 
			"Power_Handler": Power_Status, 
			"IoT_Handler": IoT_Status
		}
	}
 