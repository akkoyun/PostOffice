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
	Max_AT: Optional[MaxAT]
	
	# Min AT
	Min_AT: Optional[MinAT]

# AH Model
class AH(BaseModel):

	# Last Measured Air Humidity Value
    Value: float = Field(description="Air humidity.", example=28.3232, min=0.0, max=100.0)

	# AH Change Status
    Change: int = Field(description="Air humidity change status.", example=0, min=-1, max=1)

# AP Model
class AP(BaseModel):
    
	# Last Measured Air Pressure Value
	Value: float = Field(description="Air pressure.", example=28.3232, min=0.0, max=100.0)

	# AP Change Status
	Change: int = Field(description="Air pressure change status.", example=0, min=-1, max=1)

# R Model
class R(BaseModel):
    
	# Last 1 Hour Rain Value
	R_1: int = Field(description="1 hour rain.", example=28, min=0, max=100)

	# Last 24 Hour Rain Value
	R_24: int = Field(description="24 hour rain.", example=28, min=0, max=100)

	# Last 48 Hour Rain Value
	R_48: int = Field(description="48 hour rain.", example=28, min=0, max=100)

	# Last 168 Hour Rain Value
	R_168: int = Field(description="168 hour rain.", example=28, min=0, max=100)

# W Model
class W(BaseModel):
	
	# Last Measured Wind Speed Value
	WS: float = Field(description="Wind speed.", example=28.3232, min=0.0, max=100.0)

	# Last Measured Wind Direction Value
	WD: float = Field(description="Wind direction.", example=28.3232, min=0.0, max=360.0)

	# Wind Change Status
	Change: int = Field(description="Wind change status.", example=0, min=-1, max=1)

# UV Model
class UV(BaseModel):
	
	# Last Measured UV Value
	Value: float = Field(description="UV.", example=28.3232, min=0.0, max=100.0)
	
	# UV Change Status
	Change: int = Field(description="UV change status.", example=0, min=-1, max=1)

# 10 cm ST Model
class ST10(BaseModel):
	
	# Last Measured 10 cm Soil Temperature Value
	Value: float = Field(description="10 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 10 cm ST Change Status
	Change: int = Field(description="10 cm soil temperature change status.", example=0, min=-1, max=1)

# 30 cm ST Model
class ST30(BaseModel):
	
	# Last Measured 30 cm Soil Temperature Value
	Value: float = Field(description="30 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 30 cm ST Change Status
	Change: int = Field(description="30 cm soil temperature change status.", example=0, min=-1, max=1)

# 60 cm ST Model
class ST60(BaseModel):
	
	# Last Measured 60 cm Soil Temperature Value
	Value: float = Field(description="60 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 60 cm ST Change Status
	Change: int = Field(description="60 cm soil temperature change status.", example=0, min=-1, max=1)

# 90 cm ST Model
class ST90(BaseModel):
	
	# Last Measured 90 cm Soil Temperature Value
	Value: float = Field(description="90 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 90 cm ST Change Status
	Change: int = Field(description="90 cm soil temperature change status.", example=0, min=-1, max=1)

# ST Model
class ST(BaseModel):
	
	# 10 cm ST
	ST_10: Optional[ST10]
	
	# 30 cm ST
	ST_30: Optional[ST30]
	
	# 60 cm ST
	ST_60: Optional[ST60]
	
	# 90 cm ST
	ST_90: Optional[ST90]

# Sun Model
class Sun(BaseModel):
	
	# Sunrise
	Sunrise: datetime = Field(description="Sunrise time.", example="2022-07-19T08:28:32Z")
	
	# Sunset
	Sunset: datetime = Field(description="Sunset time.", example="2022-07-19T08:28:32Z")

# Model
class Model(BaseModel):
    
	# Device Info
	Device: Device
	
	# Air Temperature
	AT: Optional[AT]

	# Air Humidity
	AH: Optional[AH]

	# Air Pressure
	AP: Optional[AP]

	# Rain
	R: Optional[R]

	# Wind
	W: Optional[W]

	# UV
	UV: Optional[UV]
	
	# Soil Temperature
	ST: Optional[ST]

	# Sun
	Sun: Optional[Sun]

