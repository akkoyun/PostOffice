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

	# Device ID Validator
	@validator('ID')
	def ID_Validator(cls, ID_Value):

		# Define Regex Pattern
		pattern = r'^[0-9A-F]{16}$'
		
		# Check ID
		if not re.match(pattern, ID_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid ID format. Expected 'XXXXXXXXXXXXXXXX', got {ID_Value}")

		# Return ID
		return ID_Value.upper()

	# Hardware Version Validator
	@validator('Hardware')
	def Hardware_Validator(cls, Hardware_Value):

		# Define Regex Pattern
		pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'
		
		# Check Hardware
		if not re.match(pattern, Hardware_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid Hardware format. Expected 'XX.XX.XX', got {Hardware_Value}")

		# Return Hardware
		return Hardware_Value.upper()
	
	# Firmware Version Validator
	@validator('Firmware')
	def Firmware_Validator(cls, Firmware_Value):

		# Define Regex Pattern
		pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'
		
		# Check Firmware
		if not re.match(pattern, Firmware_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid Firmware format. Expected 'XX.XX.XX', got {Firmware_Value}")

		# Return Firmware
		return Firmware_Value.upper()

# Define Battery
class Pack_Battery(BaseModel):

	# Instant Battery Voltage
	IV: float = Field(..., alias="iv", description="Battery instant voltage.", example=3.8, min=0.0, max=10.0)

	# Average Battery Current
	AC: float = Field(..., alias="ac", description="Battery average current.", example=0.2, min=-10000, max=10000)

	# Battery State of Charge
	SOC: float = Field(..., alias="soc", description="Battery state of charge.", example=97.30, min=0.0, max=150.0)

	# Battery Temperature
	T: Optional[float] = Field(alias="t", default=None, description="Battery temperature.", example=32.1903, min=-50.0, max=100.0)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(alias="fb", default=None, description="Full battery capacity.", example=2000, min=0, max=10000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(alias="ib", default=None, description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery Charge State
	Charge: int = Field(..., alias="charge", description="Battery charge state.", example=1, min=0, max=10)

	# IV Validator
	@validator('IV', pre=True, always=True)
	def validate_IV(cls, value):
		
		# Check IV
		if value < 0.0 or value > 10.0:
			
			# Raise Error
			raise ValueError(f"Invalid IV value. Expected a float between 0.0 and 10.0, got {value}")
		
		# Return IV
		return value

	# AC Validator
	@validator('AC', pre=True, always=True)
	def validate_AC(cls, value):
		
		# Check AC
		if value < -10000 or value > 10000:
			
			# Raise Error
			raise ValueError(f"Invalid AC value. Expected a float between -10000 and 10000, got {value}")
		
		# Return AC
		return value

	# SOC Validator
	@validator('SOC', pre=True, always=True)
	def validate_SOC(cls, value):
		
		# Check SOC
		if value < 0.0 or value > 150.0:
			
			# Raise Error
			raise ValueError(f"Invalid SOC value. Expected a float between 0.0 and 150.0, got {value}")
		
		# Return SOC
		return value

	# T Validator
	@validator('T', pre=True, always=True)
	def validate_T(cls, value):
		
		# Check T
		if value <= -50.0 or value >= 100.0:
			
			# Raise Error
			raise ValueError(f"Invalid T value. Expected a float between -50.0 and 100.0, got {value}")
		
		# Return T
		return value

	# FB Validator
	@validator('FB', pre=True, always=True)
	def validate_FB(cls, value):
		
		# Check FB
		if value < 0 or value > 10000:
			
			# Raise Error
			raise ValueError(f"Invalid FB value. Expected an integer between 0 and 10000, got {value}")
		
		# Return FB
		return value

	# IB Validator
	@validator('IB', pre=True, always=True)
	def validate_IB(cls, value):
		
		# Check IB
		if value < 0 or value > 10000:
			
			# Raise Error
			raise ValueError(f"Invalid IB value. Expected an integer between 0 and 10000, got {value}")
		
		# Return IB
		return value

	# Charge Validator
	@validator('Charge', pre=True, always=True)
	def validate_charge(cls, value):
		
		# Check Charge
		if value < 0 or value > 10:

			# Set Charge
			return 5
		
		# Return Charge
		return value

	# Define Config
	class Config:

		# Allow Population by Field Name
		allow_population_by_field_name = True

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery = Field(..., description="Device battery.")

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(default="", description="GSM modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(default="", description="GSM modem IMEI number.", example="356156060000000")

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(default=0, description="GSM modem manufacturer ID.", example=1)

	# Module Model
	Model: Optional[int] = Field(alias="model", default=0, description="GSM modem model ID.", example=1)

	# Module Serial Number
	Serial: Optional[int] = Field(alias="serial", default=0, description="GSM modem serial ID.", example=20273)

	# GSM Firmware Validator
	@validator('Firmware')
	def Firmware_Validator(cls, Firmware_Value):

		# Define Regex Pattern
		pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{3}$'
		
		# Check Firmware
		if not re.match(pattern, Firmware_Value, re.IGNORECASE):
			
			# Raise Error
			raise ValueError(f"Invalid Firmware format. Expected 'XX.XX.XXX', got {Firmware_Value}")

		# Return Firmware
		return Firmware_Value.upper()
	
	# IMEI Validator
	@validator('IMEI')
	def IMEI_Validator(cls, IMEI_Value):

		# Define Regex Pattern
		pattern = r'^[0-9]{15}$'
		
		# Check IMEI
		if not re.match(pattern, IMEI_Value, re.IGNORECASE):
			
			# Raise Error
			raise ValueError(f"Invalid IMEI format. Expected 'XXXXXXXXXXXXXXX', got {IMEI_Value}")

		# Return IMEI
		return IMEI_Value.upper()
	
	# Manufacturer Validator
	@validator('Manufacturer')
	def Manufacturer_Validator(cls, Manufacturer_Value):

		# Check Manufacturer
		if Manufacturer_Value < 0 or Manufacturer_Value > 100:
			
			# Set Manufacturer
			Manufacturer_Value = 0

		# Return Manufacturer
		return Manufacturer_Value
	
	# Model Validator
	@validator('Model')
	def Model_Validator(cls, Model_Value):

		# Check Model
		if Model_Value < 0 or Model_Value > 100:
			
			# Set Model
			Model_Value = 0

		# Return Model
		return Model_Value
	
	# Serial Validator
	@validator('Serial')
	def Serial_Validator(cls, Serial_Value):

		# Check Serial
		if Serial_Value < 0:
			
			# Set Serial
			Serial_Value = 0

		# Return Serial
		return Serial_Value

# Define IoT Operator
class Pack_IoT_Operator(BaseModel):

	# SIM Type
	SIM_Type: Optional[int] = Field(alias="sim_type", default=None, description="SIM card type.", example=1)

	# SIM ICCID
	ICCID: str = Field(default=None, description="SIM card ICCID number.", example="8990011916180280000")

	# Operator Country Code
	MCC: Optional[int] = Field(alias="mcc", default=0, description="Operator country code.", example=286)

	# Operator Code
	MNC: Optional[int] = Field(alias="mnc", default=0, description="Operator code.", example=1)

	# RSSI
	RSSI: Optional[int] = Field(alias="rssi", default=0, description="IoT RSSI signal level.", example=28)

	# TAC
	TAC: Optional[str] = Field(default=None, description="Operator type allocation code.", example="855E")

	# LAC
	LAC: Optional[str] = Field(default=None, description="Operator base station location.", example="855E")

	# Cell ID
	Cell_ID: Optional[str] = Field(default=None, description="Operator base station cell id.", example="E678")

	# IP
	IP: Optional[str] = Field(default=None, description="IoT IP address.", example="127.0.0.1")
		
	# Connection Time
	ConnTime: Optional[int] = Field(alias="conntime", default=0, description="IoT connection time.", example=12)

	# SIM Type Validator
	@validator('SIM_Type')
	def SIM_Type_Validator(cls, SIM_Type_Value):

		# Check SIM Type
		if SIM_Type_Value < 0 or SIM_Type_Value > 100:
			
			# Set SIM Type
			SIM_Type_Value = 0

		# Return SIM Type
		return SIM_Type_Value
	
	# ICCID Validator
	@validator('ICCID')
	def ICCID_Validator(cls, ICCID_Value):

		# Define Regex Pattern
		pattern = r'^[0-9]{19}$'
		
		# Check ICCID
		if not re.match(pattern, ICCID_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid ICCID format. Expected 'XXXXXXXXXXXXXXXXXXX', got {ICCID_Value}")

		# Return ICCID
		return ICCID_Value.upper()
	
	# MCC Validator
	@validator('MCC')
	def MCC_Validator(cls, MCC_Value):

		# Check MCC
		if MCC_Value < 0 or MCC_Value > 1000:
			
			# Set MCC
			MCC_Value = 0

		# Return MCC
		return MCC_Value
	
	# MNC Validator
	@validator('MNC')
	def MNC_Validator(cls, MNC_Value):

		# Check MNC
		if MNC_Value < 0 or MNC_Value > 1000:
			
			# Set MNC
			MNC_Value = 0

		# Return MNC
		return MNC_Value
	
	# RSSI Validator
	@validator('RSSI')
	def RSSI_Validator(cls, RSSI_Value):

		# Check RSSI
		if RSSI_Value < -100 or RSSI_Value > 100:
			
			# Set RSSI
			RSSI_Value = 0

		# Return RSSI
		return RSSI_Value

	# TAC Validator
	@validator('TAC')
	def TAC_Validator(cls, TAC_Value):

		# Define Regex Pattern
		pattern = r'^[0-9A-F]{4}$'
		
		# Check TAC
		if not re.match(pattern, TAC_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid TAC format. Expected 'XXXX', got {TAC_Value}")

		# Return TAC
		return TAC_Value.upper()
	
	# LAC Validator
	@validator('LAC')
	def LAC_Validator(cls, LAC_Value):

		# Define Regex Pattern
		pattern = r'^[0-9A-F]{4}$'
		
		# Check LAC
		if not re.match(pattern, LAC_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid LAC format. Expected 'XXXX', got {LAC_Value}")

		# Return LAC
		return LAC_Value.upper()
	
	# Cell ID Validator
	@validator('Cell_ID')
	def Cell_ID_Validator(cls, Cell_ID_Value):

		# Define Regex Pattern
		pattern = r'^[0-9A-F]{4}$'
		
		# Check Cell ID
		if not re.match(pattern, Cell_ID_Value, re.IGNORECASE):
			
			raise ValueError(f"Invalid Cell ID format. Expected 'XXXX', got {Cell_ID_Value}")

		# Return Cell ID
		return Cell_ID_Value.upper()
	
	# IP Validator
	@validator('IP')
	def IP_Validator(cls, IP_Value):

		try:

			# Control for IP
			ipaddress.ip_address(IP_Value)
		
		except ipaddress.AddressValueError:

			# Raise Error			
			raise ValueError(f"Invalid IP format. Expected IPv4, got {IP_Value}")

		# Return IP
		return IP_Value
	
	# ConnTime Validator
	@validator('ConnTime')
	def ConnTime_Validator(cls, ConnTime_Value):

		# Check ConnTime
		if ConnTime_Value < 0 or ConnTime_Value > 1000:
			
			# Set ConnTime
			ConnTime_Value = 0

		# Return ConnTime
		return ConnTime_Value

# Define GSM
class Pack_GSM(BaseModel):

	# Device IoT Module
	Module: Optional[Pack_IoT_Module] = Field(description="Device IoT module.")

	# IoT Operator
	Operator: Pack_IoT_Operator = Field(description="Device IoT operator.")

# Define IoT
class Pack_IoT(BaseModel):
	
	# Device GSM
	GSM: Pack_GSM = Field(description="Device GSM.")

# Define Device
class Pack_Device(BaseModel):

	# Device Info
	Info: Pack_Info = Field(description="Device information.")

	# Device Power
	Power: Pack_Power = Field(description="Device power.")

	# Device IoT
	IoT: Pack_IoT = Field(description="Device IoT.")

# Location Definition
class Payload_WeatherStat_Location(BaseModel):
	
	# Latitude Value of Device
	Latitude: Optional[float] = Field(alias="lat", default=None, description="GNSS lattitude value.", example=1.243242342)

	# Longtitude Value of Device
	Longtitude: Optional[float] = Field(alias="lon", default=None, description="GNSS longtitude value.", example=23.3213232)

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

	# AT Validator
	@validator("AT")
	def validate_at(cls, value):
		
		# Check AT
		if value is not None and (value < -50.0 or value > 100.0):
			
			# Set AT
			value = -999

		return value

	# AH Validator
	@validator("AH")
	def validate_ah(cls, value):
		
		# Check AH
		if value is not None and (value < 0.0 or value > 100.0):

			# Set AH
			value = -999

		return value
    
	# AP Validator
	@validator("AP")
	def validate_ap(cls, value):
	
		# Check AP
		if value is not None and (value < 500.0 or value > 2000.0):

			# Set AP
			value = -999

		return value

	# VL Validator
	@validator("VL")
	def validate_vl(cls, value):

		# Check VL
		if value is not None and (value < 0 or value > 100000):

			# Set VL
			value = -999

		return value

	# IR Validator
	@validator("IR")
	def validate_ir(cls, value):
		
		# Check IR
		if value is not None and (value < 0 or value > 100000):

			# Set IR
			value = -999

		return value

	# UV Validator
	@validator("UV")
	def validate_uv(cls, value):
		
		# Check UV
		if value is not None and (value < 0.0 or value > 20.0):

			# Set UV
			value = -999

		return value

	# ST Validator
	@validator("ST")
	def validate_st(cls, value):

		# Check ST
		if value is not None:

			# Check ST
			for st in value:

				# Check ST
				if st < -50.0 or st > 100.0:

					# Set ST
					value = [-999]

		return value

	# R Validator
	@validator("R")
	def validate_r(cls, value):

		# Check R
		if value is not None and (value < 0 or value > 100000):

			# Set R
			value = -999

		return value

	# WD Validator
	@validator("WD")
	def validate_wd(cls, value):

		# Check WD
		if value is not None and (value < 0 or value > 360):

			# Set WD
			value = -999

		return value

	# WS Validator
	@validator("WS")
	def validate_ws(cls, value):

		# Check WS
		if value is not None and (value < 0.0 or value > 100.0):

			# Set WS
			value = -999

		return value

# WeatherStat Model Definition
class Payload_WeatherStat(BaseModel):

	# Location
	Location: Optional[Payload_WeatherStat_Location] = Field(description="Location.")

	# Environment
	Environment: Payload_WeatherStat_Environment = Field(description="Environment.")

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

            # Remove 'Z' if it exists
			TimeStamp_Value = TimeStamp_Value.rstrip('Z')
	
			# Convert to Datetime
			datetime.fromisoformat(TimeStamp_Value)

		except ValueError:
			
			# Raise Error
			raise ValueError(f"Invalid TimeStamp format. Expected ISO 8601 format, got {TimeStamp_Value}")
        
		# Return TimeStamp
		return TimeStamp_Value.upper()

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat] = Field(description="WeatherStat payload.")

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
	Device: Optional[Pack_Device] = Field(description="Device information.")

	# Payload
	Payload: Payload = Field(description="Payload.")