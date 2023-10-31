# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema
from Functions import Log, Kafka
from Setup.Config import APP_Settings

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.WeatherStat):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")

	# Send to Kafka Topic
	Kafka.Send_To_Topic(f"{APP_Settings.KAFKA_TOPIC_RAW}", Data.json())

	# Send Success
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={"Event": status.HTTP_200_OK},
	)
