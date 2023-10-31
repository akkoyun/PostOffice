# Library Includes
from Functions import Kafka, Log
from Setup import Database, Models
from sqlalchemy import event
from Docs.Data import Data_Update

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat, PowerStat
from datetime import datetime

# After Table Create Event
def After_Create_Table(Target, Connection, **kw):
	
	# Log Message
	Log.Terminal_Log("INFO", f"Table Created: {Target.__tablename__}")

	# Add Default SIM Items to Table
	if Target.__tablename__ == "SIM": Data_Update.Import_SIM()



# Listeners
event.listen(Database.Base.metadata, 'after_create', After_Create_Table)

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine, checkfirst=True) 








# Define FastAPI Object
PostOffice = FastAPI(version="03.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"PostOffice API Started {datetime.now()}")

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

	# Create Add Record Command
	Undefinied_RAW_Data = Models.RAW_Data(
		Client_IP = request.client.host,
		RAW_Data = exc.body,
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

	# Define DB
	DB_Module = Database.SessionLocal()

	# Service Query
	Service_PostOffice_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("PostOffice")).order_by(Models.Service_LOG.Update_Time.desc()).first()
	Service_RAW_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_RAW")).order_by(Models.Service_LOG.Update_Time.desc()).first()
	Service_WeatherStat_Status = DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like("Handler_WeatherStat")).order_by(Models.Service_LOG.Update_Time.desc()).first()

	# Get Service Status
	PostOffice_Status = Service_PostOffice_Status.Status
	RAW_Status = Service_RAW_Status.Status
	WeatherStat_Status = Service_WeatherStat_Status.Status

	# Close Database
	DB_Module.close()

	# Send Success
	return {
		"Service": "PostOffice", 
		"Version": "02.00.00", 
		"Status": {
			"PostOffice": PostOffice_Status, 
			"RAW_Handler": RAW_Status, 
			"WeatherStat_Handler": WeatherStat_Status
		}
	}
