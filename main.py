# Library Includes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from config.schema import IoT_Data_Pack_Model
from config.log_functions import Log_API_Online, Log_API_Offline, Log_API_Error, Log_API_Incomming_Data
from kafka import KafkaProducer
from json import dumps

# Define FastAPI Object
PostOffice = FastAPI()

@PostOffice.on_event("startup")
async def Startup_Event():
	Log_API_Online()

@PostOffice.on_event("shutdown")
async def Shutdown_event():
	Log_API_Offline()

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

	# Defne Kafka Producers
	Kafka_Producer = KafkaProducer(value_serializer=lambda m: dumps(m).encode('utf-8'), bootstrap_servers="165.227.154.147:9092")

	# Send Message to Queue
	Kafka_Producer.send("Error", value=str(request))

	# Print LOG
	Log_API_Error()

	return JSONResponse(
		status_code=status.HTTP_406_NOT_ACCEPTABLE,
		content={"Event": 201},
	)

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
def API(request: Request, Data: IoT_Data_Pack_Model):

	# Defne Kafka Producers
	Kafka_Producer = KafkaProducer(value_serializer=lambda m: dumps(m).encode('utf-8'), bootstrap_servers="165.227.154.147:9092")

	# Get IP
	x_forwarded_for = request.headers
	print(x_forwarded_for)

	# Set headers
	Kafka_Header = [
		('Command', bytes(Data.Command, 'utf-8')), 
		('ID', bytes(Data.Device.Info.ID, 'utf-8')), 
		('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
		('IP', bytes(ip, 'utf-8'))]

    # Send Message to Queue
	Kafka_Producer.send(topic='RAW', value=Data.dict(), headers=Kafka_Header)

	# Print LOG
	Log_API_Incomming_Data(Data.Payload.TimeStamp, Data.Device.Info.ID, Data.Command)

	# Send Success
	return {"Event": 200}