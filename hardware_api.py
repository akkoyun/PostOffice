# Library Includes
from Setup import Database, Models, Log, Config
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat, PowerStat
from kafka import KafkaProducer
import json
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
	Log.LOG_Message(f"PostOffice API Started {datetime.now()}")

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.LOG_Message(f"PostOffice API Shutdown {datetime.now()}")

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.LOG_Error_Message(f"New Undefinied Data Recieved from: {request.client.host}")

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
		Log.LOG_Message(f"Data Recorded to RAW Table")

	except Exception as e:

		# Log Message
		Log.LOG_Error_Message(f"An error occurred while adding RAW_Data: {e}")

		# Rollback DataBase
		DB_Undefinied_RAW_Data.rollback()

	finally:

		# Close Database
		DB_Undefinied_RAW_Data.close()

	# Defne Kafka Producers
	Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{Config.APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{Config.APP_Settings.POSTOFFICE_KAFKA_PORT}')

	# Send Message to Queue
	Kafka_Producer.send(topic='UNDEFINED', value=exc.body)

	# Log Message
	Log.LOG_Message("---------------------------------------")

	# Send Error
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
 		content={"Event": status.HTTP_400_BAD_REQUEST},
	)

# Include Routers
PostOffice.include_router(WeatherStat.PostOffice_WeatherStat)
PostOffice.include_router(PowerStat.PostOffice_PowerStat)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.LOG_Message(f"New Get Request: {request.client.host} - {datetime.now()}")

	# Send Success
	return {"Service": "PostOffice", "Version": "02.00.00"}
 