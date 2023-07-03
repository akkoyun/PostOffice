# Library Includes
import datetime
from Setup import Schema, Log
from fastapi import Request, status, Response, APIRouter

# Define FastAPI Object
PostOffice_Status = APIRouter()

# IoT Post Service Health Check
@PostOffice_Status.post("/Status/", status_code=status.HTTP_200_OK)
def Status(request: Request, response: Response, Data: Schema.Status_Pack_Model):

    # Control Command
    if Data.Status == "TimeStamp":

    	# Log Message
        Log.Status_TimeStamp_Log(request)

      	# Send Success
        response.status_code = status.HTTP_200_OK
        return {f"TimeStamp": datetime.datetime.now()}

    # Unknown Command
    else:

    	# Log Message
        Log.Status_Unknown_Log(request)

      	# Send Error
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Event": status.HTTP_400_BAD_REQUEST}
