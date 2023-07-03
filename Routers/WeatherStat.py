# Library Includes
from Setup import Schema, Database, Models, Log
from fastapi import Request, status, APIRouter
import json
from fastapi.responses import JSONResponse

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack_Model):

    # Handle Command
	Request_Command = Data.Command

    # Handle Company, Device and Command
	try:
		Company = Request_Command.split(":")[0]
		Device = Request_Command.split(":")[1].split(".")[0]
		Command = Request_Command.split(":")[1].split(".")[1]
	except:
		Company = "Unknown"
		Device = "Unknown"
		Command = "Unknown"

    # Device is WeatherStat
	if Device == "WeatherStat":

		# Log Message
		Log.WeatherStat_Log(Data.Device.Info.ID, Company, Device, Command)

		# Create Add Record Command
		New_Buffer = Models.Valid_Data_Buffer(
			Buffer_Device_ID = Data.Device.Info.ID,
			Buffer_Client_IP = request.client.host,
			Buffer_Company = Company,
			Buffer_Device = Device,
			Buffer_Command = Command,
			Buffer_Data = str(Data),)

		# Define DB
		DB_Buffer = Database.SessionLocal()

		# Add and Refresh DataBase
		DB_Buffer.add(New_Buffer)
		DB_Buffer.commit()
		DB_Buffer.refresh(New_Buffer)

		# Close Database
		DB_Buffer.close()

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
		New_Buffer = Models.Wrong_Data_Buffer(
			Buffer_Client_IP = request.client.host,
			Buffer_Data = str(await request.body()))

		# Define DB
		DB_Buffer = Database.SessionLocal()

		# Add and Refresh DataBase
		DB_Buffer.add(New_Buffer)
		DB_Buffer.commit()
		DB_Buffer.refresh(New_Buffer)

		# Close Database
		DB_Buffer.close()

		# Send Error
		return JSONResponse(
			status_code=status.HTTP_406_NOT_ACCEPTABLE,
			content={"Event": status.HTTP_406_NOT_ACCEPTABLE},
		)

