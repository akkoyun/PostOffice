# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("/WeatherStat/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request):

	# Send Success
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={"Event": status.HTTP_200_OK},
	)
