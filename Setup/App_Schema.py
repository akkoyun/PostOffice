# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

# Define App Base Model
# Version 01.00.00

# Device Info
class Device(BaseModel):

	# Timestamp
	LastUpdate: str = Field(description="Last Measurement time stamp.", example="2022-07-19T08:28:32Z")

# Max AT Model
class MaxAT(BaseModel):

	# Last Measured Air Temperature Value
	Value: float = Field(description="Max Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Timestamp
	Time: datetime = Field(description="Max Air temperature measurement time stamp.", example="2022-07-19T08:28:32Z")

# Min AT Model
class MinAT(BaseModel):

	# Last Measured Air Temperature Value
	Value: float = Field(description="Min Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Timestamp
	Time: datetime = Field(description="Min Air temperature measurement time stamp.", example="2022-07-19T08:28:32Z")

# AT Model
class AT(BaseModel):
    
	# Last Measured Air Temperature Value
	Value: float = Field(description="Max Air temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# AT Change Status
	Change: int = Field(description="Air temperature change status.", example=0, min=-1, max=1)

	# AT Feel Like
	AT_FL: float = Field(description="Air temperature feel like.", example=28.3232, min=-50.0, max=100.0)

	# AT Dew Point
	AT_Dew: float = Field(description="Air temperature dew point.", example=28.3232, min=-50.0, max=100.0)

	# Max AT
	Max_AT: MaxAT
	
	# Min AT
	Min_AT: MinAT

class Model(BaseModel):
    Device: Device
    AT: AT









