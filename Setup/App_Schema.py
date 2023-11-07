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

	# Device ID
	Device_ID: str = Field(description="Device ID.", example="1234567890")

	# Timestamp
	LastUpdate: datetime = Field(description="Last Measurement time stamp.", example="2022-07-19T08:28:32Z")

	# Time to Update
	TTU: int = Field(description="Time to update.", example=5)

# Max AT Model
class MaxAT(BaseModel):

	# Last Measured Air Temperature Value
	Value: Optional[float] = Field(description="Max Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Timestamp
	Time: Optional[datetime] = Field(description="Max Air temperature measurement time stamp.", example="2022-07-19T08:28:32Z")

# Min AT Model
class MinAT(BaseModel):

	# Last Measured Air Temperature Value
	Value: Optional[float] = Field(description="Min Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Timestamp
	Time: Optional[datetime] = Field(description="Min Air temperature measurement time stamp.", example="2022-07-19T08:28:32Z")

# AT Model
class AT(BaseModel):
    
	# Last Measured Air Temperature Value
	Value: Optional[float] = Field(description="Max Air temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# AT Change Status
	Change: Optional[int] = Field(description="Air temperature change status.", example=0, min=-1, max=1)

	# AT Feel Like
	AT_FL: Optional[float] = Field(description="Air temperature feel like.", example=28.3232, min=-50.0, max=100.0)

	# AT Dew Point
	AT_Dew: Optional[float] = Field(description="Air temperature dew point.", example=28.3232, min=-50.0, max=100.0)

	# Max AT
	Max_AT: Optional[MaxAT]
	
	# Min AT
	Min_AT: Optional[MinAT]

# AH Model
class AH(BaseModel):

	# Last Measured Air Humidity Value
    Value: Optional[float] = Field(description="Air humidity.", example=28.3232, min=0.0, max=100.0)

	# AH Change Status
    Change: Optional[int] = Field(description="Air humidity change status.", example=0, min=-1, max=1)

# AP Model
class AP(BaseModel):
    
	# Last Measured Air Pressure Value
	Value: Optional[float] = Field(description="Air pressure.", example=28.3232, min=0.0, max=100.0)

	# AP Change Status
	Change: Optional[int] = Field(description="Air pressure change status.", example=0, min=-1, max=1)

# R Model
class R(BaseModel):
    
	# Last 1 Hour Rain Value
	R_1: Optional[int] = Field(description="1 hour rain.", example=28, min=0, max=100)

	# Last 24 Hour Rain Value
	R_24: Optional[int] = Field(description="24 hour rain.", example=28, min=0, max=100)

	# Last 48 Hour Rain Value
	R_48: Optional[int] = Field(description="48 hour rain.", example=28, min=0, max=100)

	# Last 168 Hour Rain Value
	R_168: Optional[int] = Field(description="168 hour rain.", example=28, min=0, max=100)

# W Model
class W(BaseModel):
	
	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=28.3232, min=0.0, max=100.0)

	# Last Measured Wind Direction Value
	WD: Optional[float] = Field(description="Wind direction.", example=28.3232, min=0.0, max=360.0)

	# Wind Change Status
	Change: Optional[int] = Field(description="Wind change status.", example=0, min=-1, max=1)

# UV Model
class UV(BaseModel):
	
	# Last Measured UV Value
	Value: Optional[float] = Field(description="UV.", example=28.3232, min=0.0, max=100.0)
	
	# UV Change Status
	Change: Optional[int] = Field(description="UV change status.", example=0, min=-1, max=1)

# 10 cm ST Model
class ST_10(BaseModel):
	
	# Last Measured 10 cm Soil Temperature Value
	Value: Optional[float] = Field(description="10 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 10 cm ST Change Status
	Change: Optional[int] = Field(description="10 cm soil temperature change status.", example=0, min=-1, max=1)

# 20 cm ST Model
class ST_20(BaseModel):
	
	# Last Measured 20 cm Soil Temperature Value
	Value: Optional[float] = Field(description="20 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 20 cm ST Change Status
	Change: Optional[int] = Field(description="20 cm soil temperature change status.", example=0, min=-1, max=1)

# 30 cm ST Model
class ST_30(BaseModel):
	
	# Last Measured 30 cm Soil Temperature Value
	Value: Optional[float] = Field(description="30 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 30 cm ST Change Status
	Change: Optional[int] = Field(description="30 cm soil temperature change status.", example=0, min=-1, max=1)

# 40 cm ST Model
class ST_40(BaseModel):
	
	# Last Measured 40 cm Soil Temperature Value
	Value: Optional[float] = Field(description="40 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 40 cm ST Change Status
	Change: Optional[int] = Field(description="40 cm soil temperature change status.", example=0, min=-1, max=1)

# 50 cm ST Model
class ST_50(BaseModel):
	
	# Last Measured 50 cm Soil Temperature Value
	Value: Optional[float] = Field(description="50 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 50 cm ST Change Status
	Change: Optional[int] = Field(description="50 cm soil temperature change status.", example=0, min=-1, max=1)

# 60 cm ST Model
class ST_60(BaseModel):
	
	# Last Measured 60 cm Soil Temperature Value
	Value: Optional[float] = Field(description="60 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 60 cm ST Change Status
	Change: Optional[int] = Field(description="60 cm soil temperature change status.", example=0, min=-1, max=1)

# 70 cm ST Model
class ST_70(BaseModel):
	
	# Last Measured 70 cm Soil Temperature Value
	Value: Optional[float] = Field(description="70 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 70 cm ST Change Status
	Change: Optional[int] = Field(description="70 cm soil temperature change status.", example=0, min=-1, max=1)

# 80 cm ST Model
class ST_80(BaseModel):
	
	# Last Measured 80 cm Soil Temperature Value
	Value: Optional[float] = Field(description="80 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 80 cm ST Change Status
	Change: Optional[int] = Field(description="80 cm soil temperature change status.", example=0, min=-1, max=1)

# 90 cm ST Model
class ST_90(BaseModel):
	
	# Last Measured 90 cm Soil Temperature Value
	Value: Optional[float] = Field(description="90 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 90 cm ST Change Status
	Change: Optional[int] = Field(description="90 cm soil temperature change status.", example=0, min=-1, max=1)

# 100 cm ST Model
class ST_100(BaseModel):
	
	# Last Measured 100 cm Soil Temperature Value
	Value: Optional[float] = Field(description="100 cm soil temperature.", example=28.3232, min=-50.0, max=100.0)
	
	# 100 cm ST Change Status
	Change: Optional[int] = Field(description="100 cm soil temperature change status.", example=0, min=-1, max=1)

# ST Model
class ST(BaseModel):
	
	# 10 cm ST
	ST_10: Optional[ST_10]
	
	# 20 cm ST
	ST_20: Optional[ST_20]

	# 30 cm ST
	ST_30: Optional[ST_30]
	
	# 40 cm ST
	ST_40: Optional[ST_40]

	# 50 cm ST
	ST_50: Optional[ST_50]	

	# 60 cm ST
	ST_60: Optional[ST_60]
	
	# 70 cm ST
	ST_70: Optional[ST_70]

	# 80 cm ST
	ST_80: Optional[ST_80]

	# 90 cm ST
	ST_90: Optional[ST_90]

	# 100 cm ST
	ST_100: Optional[ST_100]

# Forecast Model
class Forecast(BaseModel):

	# Forecast Date
	Date: datetime = Field(description="Forecast date.", example="2022-07-19T08:28:32Z")

	# Forecast Time
	Time: datetime = Field(description="Forecast time.", example="2022-07-19T08:28:32Z")

	# Forecast Air Temperature
	AT: float = Field(description="Forecast air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Forecast Cloud Cover
	CC: float = Field(description="Forecast cloud cover.", example=28.3232, min=0.0, max=100.0)

	# Forecast Wind Speed
	WS: float = Field(description="Forecast wind speed.", example=28.3232, min=0.0, max=100.0)

	# Forecast Wind Direction
	WD: str = Field(description="Forecast wind direction.", example="N")

	# Forecast Rain
	CoR: float = Field(description="Forecast rain.", example=28.3232, min=0.0, max=100.0)

	# Forecast Snow
	CoS: float = Field(description="Forecast snow.", example=28.3232, min=0.0, max=100.0)

# Full Forecast Model
#class Full_Forecast(BaseModel):

	# 24 Hour Forecast


# Sun Model
class Sun(BaseModel):
	
	# Sunrise
	Sunrise: datetime = Field(description="Sunrise time.", example="2022-07-19T08:28:32Z")
	
	# Sunset
	Sunset: datetime = Field(description="Sunset time.", example="2022-07-19T08:28:32Z")

# Moon Model
class Moon(BaseModel):
	
	# Moonrise
	Moonrise: Optional[datetime] = Field(description="Moonrise time.", example="2022-07-19T08:28:32Z")

	# Moonset
	Moonset: Optional[datetime] = Field(description="Moonset time.", example="2022-07-19T08:28:32Z")

	# Moon Phase
	Phase: Optional[float] = Field(description="Moon phase.", example=20.6)

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

	# Forecast
	Forecast: Optional[Forecast]

	# Sun
	Sun: Optional[Sun]

	# Moon
	Moon: Optional[Moon]
