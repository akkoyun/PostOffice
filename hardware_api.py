# Library Includes
from Setup import Database, Models, Log, APP_Settings
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Routers import WeatherStat, PowerStat
from kafka import KafkaProducer
import json

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine) 

# Define FastAPI Object
PostOffice = FastAPI(version="02.00.00", title="PostOffice")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Start_Log()

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Stop_Log()

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Log Message
	Log.Unknown_Log(request)

	# Create Add Record Command
	RAW_Data = Models.RAW_Data(
		RAW_Data_IP = request.client.host,
		RAW_Data = exc.body,
		RAW_Data_Valid = False
	)

	# Define DB
	DB_RAW_Data = Database.SessionLocal()

	# Add Record to DataBase
	DB_RAW_Data.add(RAW_Data)
	
	# Commit DataBase
	DB_RAW_Data.commit()

	# Refresh DataBase
	DB_RAW_Data.refresh(RAW_Data)

	# Close Database
	DB_RAW_Data.close()

	# Defne Kafka Producers
	Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

	# Send Message to Queue
	Kafka_Producer.send(topic='UNDEFINED', value=exc.body)

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
	Log.Get_Log(request)

	# Send Success
	return {"Service": "PostOffice", "Version": "02.00.00"}
 