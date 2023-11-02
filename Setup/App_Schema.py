# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
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


class MinAT(BaseModel):
    Value: int
    Hour: str


class AT(BaseModel):
    Value: int
    TimeStamp: str
    Change: int
    AT_FL: int
    AT_Dew: int
    Max_AT: MaxAT
    Min_AT: MinAT


class AH(BaseModel):
    Value: int
    Change: int


class AP(BaseModel):
    Value: int
    Change: int


class R(BaseModel):
    R_0: int
    R_24: int
    R_48: int
    R_168: int


class W(BaseModel):
    WS: int
    WD: int
    Change: int


class UV(BaseModel):
    Value: int
    Change: int


class ST10(BaseModel):
    Value: int
    Change: int


class ST30(BaseModel):
    Value: int
    Change: int


class ST60(BaseModel):
    Value: int
    Change: int


class ST90(BaseModel):
    Value: int
    Change: int


class ST(BaseModel):
    ST_10: ST10
    ST_30: ST30
    ST_60: ST60
    ST_90: ST90


class Sun(BaseModel):
    Sunrise: str
    Sunset: str


class Model(BaseModel):
    Device: Device
    AT: AT
    AH: AH
    AP: AP
    R: R
    W: W
    UV: UV
    ST: ST
    Sun: Sun
