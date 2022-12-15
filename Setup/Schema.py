from pydantic import BaseModel, Field
from typing import Optional

# Define Info
class Pack_Info(BaseModel):

	# Device Hardware Version
	Hardware: Optional[str] = Field(default=None, example="01.00.00")
	
	# Device Firmware Version
	Firmware: Optional[str] = Field(default=None, example="01.00.00")
	
	# Device PCB Temperature
	Temperature: float = Field(example=28.1903)
	
	# Device PCB Humidity
	Humidity: float = Field(example=28.1903)

# Define Info
class IoT_Data_Pack_Info(Pack_Info):
	
	# Device ID
	ID: str = Field(example="8B00000000000000")

# Define Battery
class IoT_Data_Pack_Battery(BaseModel):

	# Instant Battery Voltage
	IV: float = Field(example=3.8)

	# Average Battery Current
	AC: float = Field(example=0.2)

	# Battery State of Charge
	SOC: float = Field(example=97.30)

	# Battery Charge State
	Charge: int = Field(example=3)

	# Battery Temperature
	T: Optional[float] = Field(default=None, example=32.1903)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(default=None, example=2000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(default=None, example=1820)

# Define Power
class IoT_Data_Pack_Power(BaseModel):

	# Device Battery
	Battery: IoT_Data_Pack_Battery

# Define IoT Module
class IoT_Data_Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(default="", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(default="", example="356156060000000")

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(default=1, example=1)

	# Module Model
	Model: Optional[int] = Field(default=1, example=1)

	# Module Serial Number
	Serial: Optional[str] = Field(default="", example="0000020273")

# Define IoT Operator
class IoT_Data_Pack_IoT_Operator(BaseModel):
	
	# SIM ICCID
	ICCID: Optional[str] = Field(default=None, example="8990011916180280000")

	# Operator Code
	Code: int = Field(default=0, example=28601)

	# IP
	IP: Optional[str] = Field(default=None, example="127.0.0.1")
	
	# RSSI
	RSSI: int = Field(default=0, example=28)
	
	# Connection Time
	ConnTime: Optional[int] = Field(default=0, example=12)
	
	# LAC
	LAC: Optional[str] = Field(default=None, example="855E")
	
	# Cell ID
	Cell_ID: Optional[str] = Field(default=None, example="E678")

# Define GSM
class IoT_Data_Pack_GSM(BaseModel):

	# Device IoT Module
	Module: Optional[IoT_Data_Pack_IoT_Module]

	# IoT Operator
	Operator: IoT_Data_Pack_IoT_Operator

# Define IoT
class IoT_Data_Pack_IoT(BaseModel):
	
	# Device GSM
	GSM: IoT_Data_Pack_GSM

# Pressure Model Definition
class IoT_Data_Pack_Payload_PowerStat_Pressure(BaseModel):
	
	# Min Pressure in Measurement Interval
	Min: Optional[float] = Field(default=None, example=1.25)

	# Max Pressure in Measurement Interval
	Max: Optional[float] = Field(default=None, example=3.25)

	# Avg Pressure of Measurement Interval
	Avg: Optional[float] = Field(default=None, example=2.25)

	# Last Readed Pressure in Measurement Interval
	Inst: Optional[float] = Field(default=None, example=1.89)

	# Slope of Pressure Trend in Measurement Interval
	Slope: Optional[float] = Field(default=None, example=0.12)

	# Offset of Pressure Trend in Measurement Interval
	Offset: Optional[float] = Field(default=None, example=0.85)

	# R2 of Pressure Trend in Measurement Interval
	R2: Optional[float] = Field(default=None, example=85)

	# Measured Data Count in Measurement Interval
	DataCount: Optional[int] = Field(default=None, example=22)

# Energy Model Definition
class IoT_Data_Pack_Payload_PowerStat_Energy(BaseModel):

	# Last Measured Voltage Array (R,S,T)
	Voltage: list[Optional[float]] = Field(default=None, example=[220.12, 221.23, 220.33])

	# Last Measured Current Array (R,S,T)
	Current: list[Optional[float]] = Field(default=None, example=[1.22, 1.32, 1.43])

	# Last Measured PowerFactor Average
	PowerFactor: Optional[float] = Field(default=None, example=0.85)

	# Total Energy Consumption Array in Send Interval (Active,Reactive)
	Consumption: list[Optional[float]] = Field(default=None, example=[2323, 2321])

	# Last Measured Frequency Value
	Frequency: Optional[float] = Field(default=None, example=50.21)

# PowerStat Model Definition
class IoT_Data_Pack_Payload_PowerStat(BaseModel):

	# Device Status
	DeviceStatus: int = Field(default=None, example=240)

	# Fault Status
	FaultStatus: int = Field(default=None, example=500)

	# Pressure
	Pressure: Optional[IoT_Data_Pack_Payload_PowerStat_Pressure]

	# Energy
	Energy: Optional[IoT_Data_Pack_Payload_PowerStat_Energy]

	# Falut Control List Array
	Fault: list[Optional[bool]] = Field(default=None, example=[True, True, False, False])

# Location Definition
class IoT_Data_Pack_Payload_WeatherStat_Location(BaseModel):
	
	# Latitude Value of Device
	Latitude: float = Field(default=None, example=1.243242342)

	# Longtitude Value of Device
	Longitude: float = Field(default=None, example=23.3213232)

# Environment Measurement Definition
class IoT_Data_Pack_Payload_WeatherStat_Environment(BaseModel):
	
	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(default=None, example=28.3232)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(default=None, example=85.2332)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(default=None, example=985.55)

	# Last Measured UV Value
	UV: Optional[int] = Field(default=None, example=2)

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(default=None, example=[28.12, 27.12, 26.12, 25,12])

	# Last Measured Rain Value
	R: Optional[int] = Field(default=None, example=23)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(default=None, example=275)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(default=None, example=25)

# WeatherStat Model Definition
class IoT_Data_Pack_Payload_WeatherStat(BaseModel):

	# Device Status
	DeviceStatus: int = Field(default=200, example=200)

	# Location
	Location: Optional[IoT_Data_Pack_Payload_WeatherStat_Location]

	# Environment
	Environment: IoT_Data_Pack_Payload_WeatherStat_Environment

# Define Device
class IoT_Data_Pack_Device(BaseModel):

	# Device Info
	Info: IoT_Data_Pack_Info

	# Device Power
	Power: IoT_Data_Pack_Power

	# Device IoT
	IoT: IoT_Data_Pack_IoT

# Define payload
class IoT_Data_Pack_Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(default="2022-07-19 08:28:32", example="2022-07-19 08:28:32")

	# PowerStat Payload
	PowerStat: Optional[IoT_Data_Pack_Payload_PowerStat]

	# WeatherStat Payload
	WeatherStat: Optional[IoT_Data_Pack_Payload_WeatherStat]

# Define IoT RAW Data Base Model
# PowerStat Model Version 01.02.00
# WeatherStat Model Version 01.02.00
class IoT_Data_Pack_Model(BaseModel):

	# Define Command
	Command: str = Field(default="", example="Demo:PowerStat.Online")

	# Device
	Device: IoT_Data_Pack_Device

	# Payload
	Payload: IoT_Data_Pack_Payload

