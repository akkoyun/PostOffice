# Library Includes
from Setup import Schema, Database, Models, Log
from fastapi import Request, status, APIRouter
import json
from fastapi.responses import JSONResponse
from kafka import KafkaProducer
from Setup.Config import APP_Settings
from sqlalchemy import and_
from datetime import datetime

from ..Setup import Functions as Functions


# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# Defne Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

# Handle Company
def Handle_Company(Command_String):

    # Handle Company
	try:
		Company = Command_String.split(":")[0]
	except:
		Company = "Unknown"

	# End Function
	return Company

# Handle Device
def Handle_Device(Command_String):

	# Handle Device
	try:
		Device = Command_String.split(":")[1].split(".")[0]
	except:
		Device = "Unknown"

	# End Function
	return Device

# Handle Command
def Handle_Command(Command_String):

	# Handle Command
	try:
		Command = Command_String.split(":")[1].split(".")[1]
	except:
		Command = "Unknown"

	# End Function
	return Command

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack_Model):

	# Control for Command
	try:
		Command_String = Data.Command
	except:
		Command_String = "Unknown"

	# Handle Device ID
	try:
		Device_ID = Data.Device.Info.ID
	except:
		Device_ID = "Unknown"

	# Handle Command String
	if Command_String != "Unknown":
		Company = Handle_Company(Data.Command)
		Device = Handle_Device(Data.Command)
		Command = Handle_Command(Data.Command)

	# Get Client IP
	Client_IP = request.client.host

	# Log Message
	if Command_String != "Unknown" and Device_ID != "Unknown":
		Log.WeatherStat_Log(Device_ID, Company, Device, Command)
	else:
		Log.Wrong_Device_Log(Company, Device, Command)

    # Device is WeatherStat
	if Device == "WeatherStat" and Device_ID != "Unknown":

		# Create Add Record Command
		RAW_Data = Models.RAW_Data(
			RAW_Data_Device_ID = Device_ID,
			RAW_Data_IP = Client_IP,
			RAW_Data_Company = Company,
			RAW_Data_Device = Device,
			RAW_Data_Command = Command,
			RAW_Data = await request.json()
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

		# Set headers
		Kafka_Header = [
			('Command', bytes(Command, 'utf-8')), 
			('Device_ID', bytes(Device_ID, 'utf-8')),
			('Device_Time', bytes(Data.Payload.TimeStamp, 'utf-8')), 
			('Device_IP', bytes(Client_IP, 'utf-8')),
			('Size', bytes(request.headers['content-length'], 'utf-8'))
		]

		# Send Message to Queue
		try:

			# Send Message to Queue
			Kafka_Producer.send(topic='RAW', value=Data.json(), headers=Kafka_Header).add_callback(Functions.Kafka_Send_Success).add_errback(Functions.Kafka_Send_Error)

		except Exception as e:

			# Log Message
			print(f"Failed to send RAW data: {e}")

		# Send Success
		return JSONResponse(
		    status_code=status.HTTP_200_OK,
			content={"Event": status.HTTP_200_OK},
	    )

	# Device is not WeatherStat
	else:

		# Get Body
		Body = await request.body()

		# Convert Body to String
		Body_str = Body.decode("utf-8")
		Body_dict = json.loads(Body_str)

		# Create Add Record Command
		RAW_Data = Models.RAW_Data(
			RAW_Data_Device_ID = Client_IP,
			RAW_Data = Body_dict
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

    	# Send Message to Queue
		Kafka_Producer.send(topic='UNDEFINED', value=Body_dict)

		# Send Error
		return JSONResponse(
			status_code=status.HTTP_406_NOT_ACCEPTABLE,
			content={"Event": status.HTTP_406_NOT_ACCEPTABLE},
		)

# IoT Get Method
@PostOffice_WeatherStat.get("/WeatherStat/{ID}")
def Root(request: Request, ID: str):

	# Define DB
	DB_Module = Database.SessionLocal()

	# Database Query
	Query_Module = DB_Module.query(Models.RAW_Data).filter(Models.RAW_Data.RAW_Data_Device_ID.like(ID)).order_by(Models.RAW_Data.RAW_Data_ID.desc()).first()

	# Check Query
	if not Query_Module:
		
		# Close Database
		DB_Module.close()

		# Send Error
		return JSONResponse(
			status_code=status.HTTP_404_NOT_FOUND,
			content={"Event": status.HTTP_404_NOT_FOUND},
		)
	
	else:

		# Get TimeStamp
		TimeStamp = Query_Module.RAW_Data_Create_Date.strftime("%Y-%m-%dT%H:%M:%SZ")

		# Close Database
		DB_Module.close()

		# Send Success
		return JSONResponse(
    		status_code=status.HTTP_200_OK,
    		content={"Update_Time": TimeStamp}
		)

# Battery IV Value Get Method
@PostOffice_WeatherStat.get("/WeatherStat/{ID}/IV")
def Battery_IV(request: Request, ID: str):

	# Define DB
	DB_Module = Database.SessionLocal()

	# Database Query
	Query_Battery_IV = DB_Module.query(Models.Measurement).filter(
		and_(
			Models.Measurement.Device_ID.like(ID),
			Models.Measurement.Measurement_Type_ID == 101
		)
		).order_by(Models.Measurement.Measurement_Create_Date.desc()).limit(10).all()

	# Check Query
	if not Query_Battery_IV:
		
		# Close Database
		DB_Module.close()

		# Send Error
		return JSONResponse(
			status_code=status.HTTP_404_NOT_FOUND,
			content={"Event": status.HTTP_404_NOT_FOUND},
		)
	
	else:

		# Prepare Data
		Time_Stamps = [record.Measurement_Create_Date.strftime("%Y-%m-%dT%H:%M:%SZ") for record in Query_Battery_IV]
		IV_Values = [record.Measurement_Value for record in Query_Battery_IV]

		# Close Database
		DB_Module.close()

		# Send Success
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content={"Update_Time": Time_Stamps, "IV": IV_Values}
		)
