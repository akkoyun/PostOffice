# Library Includes
from Functions import Functions, Kafka, Log
from Setup import Schema, Database, Models
from Setup.Config import APP_Settings
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from kafka import KafkaProducer
from sqlalchemy import and_
import json
from datetime import datetime

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# Defne Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack_Model):

    # Device is WeatherStat
	if Functions.Handle_Device(Data.Command) == "WEATHERSTAT":

		# Create Add Record Command
		RAW_Data = Models.RAW_Data(
			Client_IP = request.client.host,
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

		# Log Message
		Log.Terminal_Log("INFO", f"New Valid WeatherStat RAW Data Record Added: ['{request.client.host}' - '{Data.Device.Info.ID}']")

		# Close Database
		DB_RAW_Data.close()

		# Set Headers
		RAW_Header = Functions.Parse_RAW_Topic_Header(Functions.Handle_Command(Data.Command), Data.Device.Info.ID, Data.Payload.TimeStamp, request.client.host, request.headers['content-length'])

		# Send Message to Queue
		try:

			# Send Message to Queue
			Kafka.Send_To_Topic("RAW", Data.json(), RAW_Header)

		except Exception as e:

			# Log Message
			Log.Terminal_Log("ERROR", f"Failed to send RAW data: {e}")

		# Send Success
		return JSONResponse(
		    status_code=status.HTTP_200_OK,
			content={"Event": status.HTTP_200_OK},
	    )

	# Device is not Defined
	else:

		# Log Message
		Log.Terminal_Log("INFO", f"New Undefinied Data Recieved. Device: {Functions.Handle_Device(Data.Command)}")
		Log.Terminal_Log("INFO", ("---------------------------------------"))

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

# Get Method
@PostOffice_WeatherStat.get("/WeatherStat/")
def WeatherStat_Get(request: Request):

	# Log Message
	Log.Terminal_Log("INFO", f"New Get Request: {request.client.host}")

	# Send Success
	return {"Service": "WeatherStat", "Version": "01.00.00"}
