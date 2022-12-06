# Library Includes
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import asyncio, aiokafka, json
from . import Schema

# Define FastAPI Object
PostOffice = FastAPI()

# Define Loop
Kafka_Loop = asyncio.get_event_loop()

# Defne Kafka Producer
Kafka_Producer = aiokafka.AIOKafkaProducer(loop=Kafka_Loop, bootstrap_servers="165.227.154.147:9092")

@PostOffice.on_event("startup")
async def Startup_Event():

    # Wait for Kafka Start
    await Kafka_Producer.start()

    # LOG
    print("------------------------------------------------")
    print("Kafka IoT Data Producer - ONLINE")
    print("------------------------------------------------")

@PostOffice.on_event("shutdown")
async def Shutdown_event():

    # Wait for Kafka Stop
    await Kafka_Producer.stop()   

    # LOG
    print("------------------------------------------------")
    print("Kafka IoT Data Producer - OFFLINE")
    print("------------------------------------------------")

    pass

# Schema Error Handler
@PostOffice.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

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

    # Get Client IP
    client_host = request.client.host

    # Print LOG
    print("API Log -->", Data.Payload.TimeStamp, " - ", Data.Device.Info.ID, " - ", Data.Command, " --> Sended to Kafka Queue..")

    # Create Producer Object
    Kafka_Producer = request.state.Kafka_Producer

    # Handle Incomming Message
    Kafka_Message = json.dumps(Data.dict(), indent=2).encode('utf-8')

    # Send Message to Queue
    f = await Kafka_Producer.send('RAW', Kafka_Message)

    # Print LOG
    print("Kafka - ", f)

	# Send Success
    return {"Event": 200}
