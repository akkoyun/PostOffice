# Library Includes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import Kafka_Functions
from . import Schema

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
    Kafka_Functions.Kafka_Producer.send("Error", value=str(request))

    # Print LOG
    print("API Error --> Sended to Kafka Error Queue..")

    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"Event": 201},
    )

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
async def API(request: Request, Data: Schema.IoT_Data_Pack_Model):

    # Set headers
    Kafka_Header = [
        ('Command', bytes(Data.Command, 'utf-8')), 
        ('ID', bytes(Data.Device.Info.ID, 'utf-8')), 
        ('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
        ('IP', bytes(request.client.host, 'utf-8'))]

    # Print LOG
    print("API Log -->", Data.Payload.TimeStamp, " - ", Data.Device.Info.ID, " - ", Data.Command, " --> Sended to Kafka Queue..")

    # Send Message to Queue
    Kafka_Functions.Kafka_Producer.send(topic='RAW', value=Data.dict(), headers=Kafka_Header)

	# Send Success
    return {"Event": 200}
