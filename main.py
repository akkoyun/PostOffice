# Library Includes
import logging, coloredlogs
from Setup import Schema
from Setup.Config import APP_Settings
from fastapi import FastAPI, Request, status, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from kafka import KafkaProducer
import json

# Set Log Options
Service_Logger = logging.getLogger(__name__)
logging.basicConfig(filename='Log/Service.LOG', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set Log Colored
coloredlogs.install(level='DEBUG', logger=Service_Logger)

# Define FastAPI Object
PostOffice = FastAPI(version="01.00.00", title="PostOffice")

# Defne Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}")

# API Boot Sequence
@PostOffice.on_event("startup")
async def Startup_Event():

	# Log Message
	Service_Logger.debug("Service Started.")

# API ShutDown Sequence
@PostOffice.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Service_Logger.debug("Service Stopped.")

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError, Item : Body(embed=True)):

	# Set headers
	Kafka_Error_Parser_Headers = [
		('IP', bytes(request.headers['remote_addr'], 'utf-8')),
		('Size', bytes(request.headers['content-length'], 'utf-8'))]

	# Log Message
	Service_Logger.error(f"Unknown data come from device. ['{request.headers['remote_addr']}']")
	results = {"Pack": Item}
	Service_Logger.error(results)

	# Send Message to Queue
	Kafka_Producer.send("Error", value=str(request), headers=Kafka_Error_Parser_Headers)

	# Log Message
	Service_Logger.debug("Request sended to queue...")

	return JSONResponse(
		status_code=status.HTTP_406_NOT_ACCEPTABLE,
		content={"Event": 201},
	)

# IoT Get Method
@PostOffice.get("/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Send Success
	return {"STF": "IoT Backend", "Security": "Your IP is recorded for inspection."}

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
def API(request: Request, Data: Schema.IoT_Data_Pack_Model):

	# Set headers
	Kafka_Header = [
		('Command', bytes(Data.Command, 'utf-8')), 
		('Device_ID', bytes(Data.Device.Info.ID, 'utf-8')), 
		('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
		('Device_IP', bytes(request.headers['remote_addr'], 'utf-8')),
		('Size', bytes(request.headers['content-length'], 'utf-8'))]

    # Send Message to Queue
	Kafka_Producer.send(topic='RAW', value=Data.dict(), headers=Kafka_Header)

	# Log Message
	Service_Logger.debug(f"Incomming data from ['{Data.Device.Info.ID}'] with ['{Data.Command}'] at ['{Data.Payload.TimeStamp}']")

	# Send Success
	return {"Event": 200}