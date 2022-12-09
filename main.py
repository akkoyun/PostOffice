# Library Includes
from fastapi import FastAPI, Request, status
from config.schema import IoT_Data_Pack_Model
from kafka import KafkaProducer
from json import dumps

# Define FastAPI Object
PostOffice = FastAPI()

# IoT Post Method
@PostOffice.post("/", status_code=status.HTTP_201_CREATED)
def API(request: Request, Data: IoT_Data_Pack_Model):

	# Defne Kafka Producers
	Kafka_Producer = KafkaProducer(value_serializer=lambda m: dumps(m).encode('utf-8'), bootstrap_servers="165.227.154.147:9092")

	# Set headers
	Kafka_Header = [
		('Command', bytes(Data.Command, 'utf-8')), 
		('ID', bytes(Data.Device.Info.ID, 'utf-8')), 
		('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
		('IP', bytes(request.client.host, 'utf-8'))]

    # Send Message to Queue
	Kafka_Producer.send(topic='RAW', value=Data.dict(), headers=Kafka_Header)

	# Print LOG
	print("Incomming Data -->", Data.Payload.TimeStamp, " : ", Data.Device.Info.ID, " - ", Data.Command, " --> Sended to Queue..")

	# Send Success
	return {"Event": 200}