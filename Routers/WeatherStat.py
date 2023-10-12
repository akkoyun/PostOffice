# Library Includes
from Setup import Schema, Database, Models, Log
from fastapi import Request, status, APIRouter
import json
from fastapi.responses import JSONResponse
from kafka import KafkaProducer
from Setup.Config import APP_Settings

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack_Model):

    # Handle Company
	try:
		Company = Data.Command.split(":")[0]		
	except:
		Company = "Unknown"

	# Handle Device
	try:
		Device = Data.Command.split(":")[1].split(".")[0]
	except:
		Device = "Unknown"

	# Handle Command
	try:
		Command = Data.Command.split(":")[1].split(".")[1]
	except:
		Command = "Unknown"


    # Device is WeatherStat
	if Device == "WeatherStat":

		# Log Message
		Log.WeatherStat_Log(Data.Device.Info.ID, Company, Device, Command)

		# Defne Kafka Producers
		Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}")

		# Set headers
		Kafka_Header = [
			('Command', bytes(Data.Command, 'utf-8')), 
			('Device_ID', bytes(Data.Device.Info.ID, 'utf-8')),
			('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
			('Device_IP', bytes(request.headers['remote_addr'], 'utf-8')),
			('Size', bytes(request.headers['content-length'], 'utf-8'))
		]

    	# Send Message to Queue
		Kafka_Producer.send(topic='RAW', value=Data.dict(), headers=Kafka_Header)

		# Create Add Record Command
		RAW_Data = Models.RAW_Data(
			RAW_Data_Device_ID = Data.Device.Info.ID,
			RAW_Data_IP = request.client.host,
			RAW_Data_Company = Company,
			RAW_Data_Device = Device,
			RAW_Data_Command = Command,
			RAW_Data = await request.json()
		)
	
		# Define DB
		DB_RAW_Data = Database.SessionLocal()

		# Add and Refresh DataBase
		DB_RAW_Data.add(RAW_Data)
		DB_RAW_Data.commit()
		DB_RAW_Data.refresh(RAW_Data)

		# Close Database
		DB_RAW_Data.close()

		# Send Success
		return JSONResponse(
		    status_code=status.HTTP_200_OK,
			content={"Event": status.HTTP_200_OK},
	    )

	# Device is not WeatherStat
	else:

		# Log Messageü
		Log.Wrong_Device_Log(Company, Device, Command)

		# Create Add Record Command
		RAW_Data = Models.RAW_Data(
			RAW_Data_Device_ID = request.client.host,
			RAW_Data = await request.body()
		)

		# Define DB
		DB_RAW_Data = Database.SessionLocal()

		# Add and Refresh DataBase
		DB_RAW_Data.add(RAW_Data)
		DB_RAW_Data.commit()
		DB_RAW_Data.refresh(RAW_Data)

		# Close Database
		DB_RAW_Data.close()

		# Send Error
		return JSONResponse(
			status_code=status.HTTP_406_NOT_ACCEPTABLE,
			content={"Event": status.HTTP_406_NOT_ACCEPTABLE},
		)

# IoT Get Method
@PostOffice_WeatherStat.get("/WeatherStat/", status_code=status.HTTP_200_OK)
def Root(request: Request):

	# Log Message
	Log.Get_Log(request)

	# Send Success
	return {"Service": "WeatherStat", "Version": "02.00.00"}
