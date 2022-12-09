# Library Includes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Setup.Config import KafkaProducer as Kafka_Producer
from . import Schema
from kafka.errors import KafkaError

# Define FastAPI Object
PostOffice = FastAPI()

@PostOffice.on_event("startup")
async def Startup_Event():

    # LOG
    print("------------------------------------------------")
    print("Kafka IoT Data Producer - ONLINE")
    print("------------------------------------------------")

@PostOffice.on_event("shutdown")
async def Shutdown_event():

    # LOG
    print("------------------------------------------------")
    print("Kafka IoT Data Producer - OFFLINE")
    print("------------------------------------------------")

    pass

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    # Send Message to Queue
    Kafka_Producer.send("Error", value=str(request))

    # LOG
    print("Error..")

    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"Event": 201},
    )

# inject producer object to each request
@PostOffice.middleware("http")
async def kafka_middleware(request: Request, call_next):
    global Kafka_Producer 
    request.state.Kafka_Producer = Kafka_Producer
    response = await call_next(request)
    return response

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
async def API(request: Request, Data: Schema.IoT_Data_Pack_Model):

    # Handle Headers
    Command = Data.Command
    Device_ID = Data.Device.Info.ID
    Device_Time = Data.Payload.TimeStamp
    Device_IP = request.client.host

    # Set headers
    Kafka_Header = [
        ('Command', bytes(Command, 'utf-8')), 
        ('ID', bytes(Device_ID, 'utf-8')), 
        ('Device_Time', bytes(Device_Time, 'utf-8')), 
        ('IP', bytes(Device_IP, 'utf-8'))]

    # Print LOG
    print("API Log -->", Data.Payload.TimeStamp, " - ", Data.Device.Info.ID, " - ", Data.Command, " --> Sended to Kafka Queue..")

    # Send Message to Queue
    Kafka_Producer.send("RAW", value=Data.dict(), headers=Kafka_Header)

	# Send Success
    return {"Event": 200}
