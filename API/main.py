# Library Includes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from . import Schema
from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Define FastAPI Object
PostOffice = FastAPI()

# Defne Kafka Producer
Kafka_Producer = KafkaProducer(
    value_serializer=lambda m: dumps(m).encode('utf-8'),
    bootstrap_servers="165.227.154.147:9092")

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
async def validation_exception_handler(params: Text2kgParams):

    # Send Message to Queue
    Kafka_Producer.send("Error", params.text)

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

    # Print LOG
    print("API Log -->", Data.Payload.TimeStamp, " - ", Data.Device.Info.ID, " - ", Data.Command, " --> Sended to Kafka Queue..")

    # Set Message Header
    Kafka_Message_Headers = [('Command', bytes(Data.Command, 'utf-8')), ('ID', bytes(Data.Device.Info.ID, 'utf-8')), ('IP', bytes(request.client.host, 'utf-8'))]

    try:

        # Send Message to Queue
        Kafka_Producer.send("RAW", value=Data.dict(), headers=Kafka_Message_Headers)

    except KafkaError as exc:

        print("Exception during getting assigned partitions - {}".format(exc))

        pass

	# Send Success
    return {"Event": 200}
