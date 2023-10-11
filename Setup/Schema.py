from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

# Define Status Check Base Model
# Version 01.00.00

# Define Charge_State
class Charge_State_Class(Enum):
	Not_Charging = 0
	Pre_Charging = 1
	Fast_Charging = 2
	Charge_Done = 3

# Define SIM_Type
class SIM_Type_Class(Enum):
	Unknown = 0
	Normal_SIM = 1
	Micro_SIM = 2
	Nano_SIM = 3
	Embedded_SIM = 4
	Removable_eSIM = 5

# Define Info
class Pack_Info(BaseModel):

	# Device ID
	ID: str = Field(example="8B00000000000000", description="IoT device unique ID.")

	# Device Hardware Version
	Hardware: Optional[str] = Field(default=None, description="Hardware version of device.", example="01.00.00", min_length=5, max_length=8)
	
	# Device Firmware Version
	Firmware: Optional[str] = Field(default=None, description="Firmware version of device.", example="01.00.00", min_length=5, max_length=8)

# Define Battery
class Pack_Battery(BaseModel):

	# Instant Battery Voltage
	IV: float = Field(description="Battery instant voltage.", example=3.8, min=0.0, max=5.0)

	# Average Battery Current
	AC: float = Field(description="Battery average current.", example=0.2)

	# Battery State of Charge
	SOC: float = Field(description="Battery state of charge.", example=97.30, min=0.0, max=100.0)

	# Battery Temperature
	T: Optional[float] = Field(default=None, description="Battery temperature.", example=32.1903, min=-40.0, max=85.0)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(default=None, description="Full battery capacity.", example=2000, min=0, max=10000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(default=None, description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery Charge State
	Charge: Charge_State_Class = Field(description="Battery charge state.", example=Charge_State_Class.Charge_Done, min=0, max=3)

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(default="", description="GSM modem firmware version.", example="13.00.007", min_length=5, max_length=10)

	# Module IMEI Number
	IMEI: Optional[str] = Field(default="", description="GSM modem IMEI number.", example="356156060000000", min_length=12, max_length=16)

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(default=0, description="GSM modem manufacturer ID.", example=1, min=0, max=5)

	# Module Model
	Model: Optional[int] = Field(default=0, description="GSM modem model ID.", example=1, min=0, max=5)

	# Module Serial Number
	Serial: Optional[str] = Field(default="", description="GSM modem serial ID.", example="0000020273", min_length=1, max_length=10)

# Define IoT Operator
class Pack_IoT_Operator(BaseModel):

	# SIM Type
	SIM_Type: Optional[SIM_Type_Class] = Field(default=None, description="SIM card type.", example=SIM_Type_Class.Normal_SIM, min=0, max=5)

	# SIM ICCID
	ICCID: str = Field(default=None, description="SIM card ICCID number.", example="8990011916180280000")

	# Operator Country Code
	MCC: int = Field(default=0, description="Operator country code.", example=286, min=0, max=999)

	# Operator Code
	MNC: int = Field(default=0, description="Operator code.", example=1, min=0, max=99)

	# RSSI
	RSSI: int = Field(default=0, description="IoT RSSI signal level.", example=28, min=0, max=100)

	# TAC
	TAC: Optional[str] = Field(default=None, description="Operator type allocation code.", example="855E", min_length=4, max_length=4)

	# LAC
	LAC: Optional[str] = Field(default=None, description="Operator base station location.", example="855E", min_length=4, max_length=4)

	# Cell ID
	Cell_ID: Optional[str] = Field(default=None, description="Operator base station cell id.", example="E678", min_length=4, max_length=4)

	# IP
	IP: Optional[str] = Field(default=None, description="IoT IP address.", example="127.0.0.1", min_length=7, max_length=15)
		
	# Connection Time
	ConnTime: Optional[int] = Field(default=0, description="IoT connection time.", example=12, min=0, max=500)

# Define GSM
class Pack_GSM(BaseModel):

	# Device IoT Module
	Module: Optional[Pack_IoT_Module]

	# IoT Operator
	Operator: Pack_IoT_Operator

# Define IoT
class Pack_IoT(BaseModel):
	
	# Device GSM
	GSM: Pack_GSM

# Define Device
class Pack_Device(BaseModel):

	# Device Info
	Info: Pack_Info

	# Device Power
	Power: Pack_Power

	# Device IoT
	IoT: Pack_IoT

# Location Definition
class Payload_WeatherStat_Location(BaseModel):
	
	# Latitude Value of Device
	Latitude: float = Field(default=None, description="GNSS lattitude value.", example=1.243242342)

	# Longtitude Value of Device
	Longtitude: float = Field(default=None, description="GNSS longtitude value.", example=23.3213232)

# Environment Measurement Definition
class Payload_WeatherStat_Environment(BaseModel):
	
	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(default=None, description="Air temperature.", example=28.3232, min=-40.0, max=85.0)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(default=None, description="Air humidity.", example=85.2332, min=0.0, max=100.0)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(default=None, description="Air pressure.", example=985.55, min=0.0, max=5000.0)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(default=None, description="Visual light.", example=2, min=0)

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(default=None, description="Infrared light.", example=2, min=0)

	# Last Measured UV Value
	UV: Optional[float] = Field(default=None, description="UV index.", example=2, min=0)

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(default=None, description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=1, max_items=10)

	# Last Measured Rain Value
	R: Optional[int] = Field(default=None, description="Rain tip counter.", example=23, min=0, max=1000)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(default=None, description="Wind direction.", example=275, min=0, max=360)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(default=None, description="Wind speed.", example=25, min=0.0, max=100.0)

# WeatherStat Model Definition
class Payload_WeatherStat(BaseModel):

	# Location
	Location: Optional[Payload_WeatherStat_Location]

	# Environment
	Environment: Payload_WeatherStat_Environment

# Define payload
class Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(
		default="2022-07-19T08:28:32Z", 
		description="Measurement time stamp.", 
		example="2022-07-19T08:28:32Z", 
		min_length=10, 
		max_length=20
	)

	# TimeStamp Validator
	@validator('TimeStamp')
	def Validator(cls, value):
		try:
			# Convert TimeStamp to Datetime
			datetime.fromisoformat(value)
		except ValueError:
			raise ValueError('Incorrect data format, should be YYYY-MM-DDThh:mm:ssZ')
		return value

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat]

# Define IoT RAW Data Base Model
# PowerStat Model Version 01.03.00
# WeatherStat Model Version 01.03.00
class Data_Pack_Model(BaseModel):

	# Define Schema
	_Schema: Optional[str] = Field(..., alias="$schema")

	# Define Command
	Command: str = Field(default="", description="Pack command.", example="Demo:PowerStat.Online", min_length=8, max_length=32)

	# Device
	Device: Optional[Pack_Device]

	# Payload
	Payload: Payload
