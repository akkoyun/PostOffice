from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime

# Define Status Check Base Model
# Version 01.00.00

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
	Charge: int = Field(description="Battery charge state.", example=1, min=0, max=5)

	# Charge State Validator
	def __init__(self, **data):
		Charge_Value = data.get('Charge', 5)
		if Charge_Value < 0 or Charge_Value > 5:
			data['Charge'] = 5
		super().__init__(**data)

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(default="", description="GSM modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(default="", description="GSM modem IMEI number.", example="356156060000000")

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(default=0, description="GSM modem manufacturer ID.", example=1)

	# Module Model
	Model: Optional[int] = Field(default=0, description="GSM modem model ID.", example=1)

	# Module Serial Number
	Serial: Optional[str] = Field(default="", description="GSM modem serial ID.", example="0000020273")

# Define IoT Operator
class Pack_IoT_Operator(BaseModel):

	# SIM Type
	SIM_Type: Optional[int] = Field(default=None, description="SIM card type.", example=1)

	# SIM ICCID
	ICCID: str = Field(default=None, description="SIM card ICCID number.", example="8990011916180280000")

	# Operator Country Code
	MCC: Optional[int] = Field(default=0, description="Operator country code.", example=286)

	# Operator Code
	MNC: Optional[int] = Field(default=0, description="Operator code.", example=1)

	# RSSI
	RSSI: Optional[int] = Field(default=0, description="IoT RSSI signal level.", example=28)

	# TAC
	TAC: Optional[str] = Field(default=None, description="Operator type allocation code.", example="855E")

	# LAC
	LAC: Optional[str] = Field(default=None, description="Operator base station location.", example="855E")

	# Cell ID
	Cell_ID: Optional[str] = Field(default=None, description="Operator base station cell id.", example="E678")

	# IP
	IP: Optional[str] = Field(default=None, description="IoT IP address.", example="127.0.0.1")
		
	# Connection Time
	ConnTime: Optional[int] = Field(default=0, description="IoT connection time.", example=12)

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
	AT: Optional[float] = Field(default=None, description="Air temperature.", example=28.3232)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(default=None, description="Air humidity.", example=85.2332)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(default=None, description="Air pressure.", example=985.55)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(default=None, description="Visual light.")

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(default=None, description="Infrared light.")

	# Last Measured UV Value
	UV: Optional[float] = Field(default=None, description="UV index.")

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(default=None, description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=1, max_items=10)

	# Last Measured Rain Value
	R: Optional[int] = Field(default=None, description="Rain tip counter.", example=23)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(default=None, description="Wind direction.", example=275)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(default=None, description="Wind speed.", example=25)

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
		example="2022-07-19T08:28:32Z"
	)

    # TimeStamp Validator
	@validator('TimeStamp')
	def validate_timestamp(cls, TimeStamp_Value):

		try:

			# Convert to Datetime
			datetime.fromisoformat(TimeStamp_Value)

		except ValueError:
			
			# Raise Error
			raise ValueError(f"Invalid TimeStamp format. Expected ISO 8601 format, got {TimeStamp_Value}")
        
		# Return TimeStamp
		return TimeStamp_Value

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat]

# Define IoT RAW Data Base Model
# PowerStat Model Version 01.03.00
# WeatherStat Model Version 01.03.00
class Data_Pack_Model(BaseModel):

	# Define Schema
	_Schema: Optional[str] = Field(..., alias="$schema")

	# Define Command
	Command: str = Field(default="", description="Pack command.", example="Demo:PowerStat.Online")

	# Command Validator
	@validator('Command')
	def Command_Validator(cls, Command_Value):

		# Define Regex Pattern
		pattern = r'^[a-zA-Z]+:[a-zA-Z]+\.[a-zA-Z]+$'
        
		# Check Command
		if not re.match(pattern, Command_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid command format. Expected 'xxx:yyy.zzz', got {Command_Value}")

		# Return Command
		return Command_Value.upper()

	# Device
	Device: Optional[Pack_Device]

	# Payload
	Payload: Payload
