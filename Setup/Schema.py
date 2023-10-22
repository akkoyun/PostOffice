from pydantic import BaseModel, Field, validator
from typing import Optional
import re, ipaddress
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
	IV: float = Field(alias="iv", description="Battery instant voltage.", example=3.8, min=0.0, max=10.0)

	# Average Battery Current
	AC: float = Field(alias="ac", description="Battery average current.", example=0.2, min=-10000, max=10000)

	# Battery State of Charge
	SOC: float = Field(alias="soc", description="Battery state of charge.", example=97.30, min=0.0, max=150.0)

	# Battery Temperature
	T: Optional[float] = Field(alias="t", default=None, description="Battery temperature.", example=32.1903, min=-50.0, max=100.0)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(alias="fb", default=None, description="Full battery capacity.", example=2000, min=0, max=10000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(alias="ib", default=None, description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery Charge State
	Charge: int = Field(alias="charge", description="Battery charge state.", example=1, min=0, max=10)

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery = Field(..., alias="battery", description="Device battery.")

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(alias="firmware", default="", description="GSM modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(alias="imei", default="", description="GSM modem IMEI number.", example="356156060000000")

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(alias="manufacturer", default=0, description="GSM modem manufacturer ID.", example=1)

	# Module Model
	Model: Optional[int] = Field(alias="model", default=0, description="GSM modem model ID.", example=1)

	# Module Serial Number
	Serial: Optional[int] = Field(alias="serial", default=0, description="GSM modem serial ID.", example=20273)

# Define IoT Operator
class Pack_IoT_Operator(BaseModel):

	# SIM Type
	SIM_Type: Optional[int] = Field(alias="sim_type", default=None, description="SIM card type.", example=1)

	# SIM ICCID
	ICCID: str = Field(alias="iccid", default=None, description="SIM card ICCID number.", example="8990011916180280000")

	# Operator Country Code
	MCC: Optional[int] = Field(alias="mcc", default=0, description="Operator country code.", example=286)

	# Operator Code
	MNC: Optional[int] = Field(alias="mnc", default=0, description="Operator code.", example=1)

	# RSSI
	RSSI: Optional[int] = Field(alias="rssi", default=0, description="IoT RSSI signal level.", example=28)

	# TAC
	TAC: Optional[str] = Field(alias="tac", default=None, description="Operator type allocation code.", example="855E")

	# LAC
	LAC: Optional[str] = Field(alias="lac", default=None, description="Operator base station location.", example="855E")

	# Cell ID
	Cell_ID: Optional[str] = Field(alias="cell_id", default=None, description="Operator base station cell id.", example="E678")

	# IP
	IP: Optional[str] = Field(alias="ip", default=None, description="IoT IP address.", example="127.0.0.1")
		
	# Connection Time
	ConnTime: Optional[int] = Field(alias="conntime", default=0, description="IoT connection time.", example=12)

# Define GSM
class Pack_GSM(BaseModel):

	# Device IoT Module
	Module: Optional[Pack_IoT_Module] = Field(default=None, alias="module", description="Device IoT module.")

	# IoT Operator
	Operator: Pack_IoT_Operator = Field(default=None, alias="operator", description="Device IoT operator.")

# Define IoT
class Pack_IoT(BaseModel):
	
	# Device GSM
	GSM: Pack_GSM = Field(..., alias="gsm", description="Device GSM.")

# Define Device
class Pack_Device(BaseModel):

	# Device Info
	Info: Pack_Info = Field(..., alias="info", description="Device information.")

	# Device Power
	Power: Pack_Power = Field(..., alias="power", description="Device power.")

	# Device IoT
	IoT: Pack_IoT = Field(..., alias="iot", description="Device IoT.")

# Location Definition
class Payload_WeatherStat_Location(BaseModel):
	
	# Latitude Value of Device
	Latitude: float = Field(alias="lat", default=None, description="GNSS lattitude value.", example=1.243242342)

	# Longtitude Value of Device
	Longtitude: float = Field(alias="lon", default=None, description="GNSS longtitude value.", example=23.3213232)

# Environment Measurement Definition
class Payload_WeatherStat_Environment(BaseModel):
	
	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(alias="at", default=None, description="Air temperature.", example=28.3232)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(alias="ah", default=None, description="Air humidity.", example=85.2332)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(alias="ap", default=None, description="Air pressure.", example=985.55)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(alias="vl", default=None, description="Visual light.")

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(alias="ir", default=None, description="Infrared light.")

	# Last Measured UV Value
	UV: Optional[float] = Field(alias="uv", default=None, description="UV index.")

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(alias="st", default=None, description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=1, max_items=10)

	# Last Measured Rain Value
	R: Optional[int] = Field(alias="r", default=None, description="Rain tip counter.", example=23)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(alias="wd", default=None, description="Wind direction.", example=275)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(alias="ws", default=None, description="Wind speed.", example=25)

# WeatherStat Model Definition
class Payload_WeatherStat(BaseModel):

	# Location
	Location: Optional[Payload_WeatherStat_Location] = Field(description="Location.")

	# Environment
	Environment: Payload_WeatherStat_Environment = Field(description="Environment.")

# Define payload
class Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(default="2022-07-19T08:28:32Z", description="Measurement time stamp.", example="2022-07-19T08:28:32Z")

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat] = Field(description="WeatherStat payload.")

# Define IoT RAW Data Base Model
# PowerStat Model Version 01.03.00
# WeatherStat Model Version 01.03.00
class Data_Pack_Model(BaseModel):

	# Define Schema
	_Schema: Optional[str] = Field(alias="$schema")

	# Define Command
	Command: str = Field(default="", description="Pack command.", example="Demo:PowerStat.Online")

	# Device
	Device: Optional[Pack_Device] = Field(description="Device information.")

	# Payload
	Payload: Payload = Field(description="Payload.")
