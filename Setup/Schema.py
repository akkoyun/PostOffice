# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, root_validator
from typing import Optional, Dict, List
import re, ipaddress
from datetime import datetime

# Define Status Check Base Model
# Version 01.00.00

# Define Info
class Pack_Info(BaseModel):

	# Device ID
	ID: str = Field(example="8B00000000000000", description="IoT device unique ID.")

	# Device Hardware Version
	Hardware: Optional[str] = Field(description="Hardware version of device.", example="01.00.00")

	# Device Firmware Version
	Firmware: Optional[str] = Field(description="Firmware version of device.", example="01.00.00")

# Define Battery
class Pack_Battery(BaseModel):

	# Instant Battery Voltage
	IV: float = Field(description="Battery instant voltage.", example=3.8, min=0.0, max=10.0)

	# Average Battery Current
	AC: float = Field(description="Battery average current.", example=0.2, min=-10000.0, max=10000.0)

	# Battery State of Charge
	SOC: float = Field(description="Battery state of charge.", example=97.30, min=0.0, max=100.0)

	# Battery Temperature
	T: Optional[float] = Field(description="Battery temperature.", example=32.1903, min=-50.0, max=100.0)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(description="Full battery capacity.", example=2000, min=0, max=10000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery Charge State
	Charge: int = Field(description="Battery charge state.", example=1, min=0, max=5)

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(description="GSM modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(description="GSM modem IMEI number.", example="356156060000000", min_length=10, max_length=15)

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(description="GSM modem manufacturer ID.", example=1, min=0, max=100)

	# Module Model
	Model: Optional[int] = Field(description="GSM modem model ID.", example=1, min=0, max=100)

	# Module Serial Number
	Serial: Optional[int] = Field(description="GSM modem serial ID.", example=20273, min=0)

# Define IoT Operator
class Pack_IoT_Operator(BaseModel):

	# SIM Type
	SIM_Type: Optional[int] = Field(description="SIM card type.", example=1, min=0, max=10)

	# SIM ICCID
	ICCID: str = Field(description="SIM card ICCID number.", example="8990011916180280000", min_length=10, max_length=20)

	# Operator Country Code
	MCC: Optional[int] = Field(description="Operator country code.", example=286, min=0, max=1000)

	# Operator Code
	MNC: Optional[int] = Field(description="Operator code.", example=1, min=0, max=1000)

	# RSSI
	RSSI: Optional[int] = Field(description="IoT RSSI signal level.", example=28, min=-100, max=100)

	# TAC
	TAC: Optional[str] = Field(description="Operator type allocation code.", example="855E", min_length=3, max_length=5)

	# LAC
	LAC: Optional[str] = Field(description="Operator base station location.", example="855E", min_length=3, max_length=5)

	# Cell ID
	Cell_ID: Optional[str] = Field(description="Operator base station cell id.", example="E678", min_length=3, max_length=5)

	# IP
	IP: Optional[str] = Field(description="IoT IP address.", example="127.0.0.1", min_length=7, max_length=15)

	# Connection Time
	ConnTime: Optional[int] = Field(description="IoT connection time.", example=12, min=0, max=100000)

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
	Latitude: float = Field(description="GNSS lattitude value.", example=1.243242342)

	# Longtitude Value of Device
	Longtitude: float = Field(description="GNSS longtitude value.", example=23.3213232)

# Environment Measurement Definition
class Payload_WeatherStat_Environment(BaseModel):
	
	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(description="Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(description="Air humidity.", example=85.2332, min=0.0, max=100.0)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(description="Air pressure.", example=985.55, min=500.0, max=2000.0)

	# Last Measured UV Value
	UV: Optional[float] = Field(description="UV index.", example=2.12, min=0.0, max=20.0)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(description="Visual light.", example=1234, min=0, max=100000)

	# Last Measured Infrared Light Value
	IL: Optional[int] = Field(description="Infrared light.", example=1234, min=0, max=100000)

	# Last Measured Soil Temperature Value
	ST: Optional[list[float]] = Field(description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], max_items=10, min=-50.0, max=100.0)

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23, min=0, max=100000)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25, min=0.0, max=100.0)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275, min=0, max=360)

# WeatherStat Model Definition
class Payload_WeatherStat(BaseModel):

	# Location
	Location: Optional[Payload_WeatherStat_Location]

	# Environment
	Environment: Payload_WeatherStat_Environment

# Define payload
class Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(description="Measurement time stamp.", example="2022-07-19T08:28:32Z")

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat]

# Define IoT RAW Data Base Model
# WeatherStat Model Version 01.03.00
class Data_Pack_Model(BaseModel):

	# Define Command
	Command: str = Field(description="Pack command.", example="Demo:PowerStat.Online")

	# Device
	Device: Optional[Pack_Device]

	# Payload
	Payload: Payload
