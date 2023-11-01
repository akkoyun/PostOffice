# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime

# Define Status Check Base Model
# Version 01.00.00

# Define Info
class Info(BaseModel):

	# Define Command
	Command: str = Field(description="Pack command.", example="Online")
    
	# Timestamp
	TimeStamp: str = Field(description="Measurement time stamp.", example="2022-07-19T08:28:32Z")
	
	# Device ID
	ID: str = Field(description="IoT device unique ID.", example="8B00000000000000")
	
	# Device Firmware Version
	Firmware: Optional[str] = Field(description="Firmware version of device.", example="01.00.00")

	# Command Validator
	@validator("Command", pre=True, always=True)
	def Validate_Command(cls, command):

		# Define Allowed Commands
		Allowed_Commands = ["Online", "Offline", "Timed"]

		# Return Command
		return command if command in Allowed_Commands else "Unknown"

	# Device ID Validator
	@validator('ID', pre=True, always=True)
	def ID_Validator(cls, ID_Value):

		# Define Regex Pattern
		Pattern = r'^[0-9A-F]{10,16}$'

		# Check ID
		if not re.match(Pattern, ID_Value):

			# Raise Error
			raise ValueError(f"Invalid ID format. Expected 'XXXXXXXXXXXXXXXX', got {ID_Value}")

		# Return ID
		return ID_Value

	# Firmware Validator
	@validator('Firmware', pre=True, always=True)
	def Version_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid version format. Expected 'XX.XX.XX', got {Value}")

		# Return Value
		return Value

# Define Power
class Power(BaseModel):
	
	# Instant Battery Voltage
	B_IV: float = Field(description="Battery instant voltage.", example=3.8, min=0.0, max=6.0)

	# Average Battery Current
	B_AC: float = Field(description="Battery average current.", example=0.2, min=-5000, max=5000)

	# Full Battery Capacity
	B_FC: Optional[int] = Field(description="Full battery capacity.", example=2000, min=0, max=10000)

	# Instant Battery Capacity
	B_IC: Optional[int] = Field(description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery State of Charge
	B_SOC: float = Field(description="Battery state of charge.", example=97.30, min=0.0, max=100.0)

	# Battery Temperature
	B_T: Optional[float] = Field(description="Battery temperature.", example=32.1903, min=-50.0, max=100.0)

	# Battery Charge State
	B_CS: int = Field(description="Battery charge state.", example=1, min=0, max=5)

	# Battery Instant Voltage Validator
	@validator('B_IV', pre=True, always=True)
	def B_IV_Validator(cls, Value):

		# Check Value
		if not 0.0 <= Value <= 6.0:

			# Raise Error
			raise ValueError(f"Invalid battery instant voltage. Expected '0.0 - 6.0', got {Value}")

		# Return Value
		return Value
	
	# Battery Average Current Validator
	@validator('B_AC', pre=True, always=True)
	def B_AC_Validator(cls, Value):

		# Check Value
		if not -5000 <= Value <= 5000:

			# Raise Error
			raise ValueError(f"Invalid battery average current. Expected '-5000 - 5000', got {Value}")

		# Return Value
		return Value
	
	# Full Battery Capacity Validator
	@validator('B_FC', pre=True, always=True)
	def B_FC_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 10000:

			# Raise Error
			raise ValueError(f"Invalid full battery capacity. Expected '0 - 10000', got {Value}")

		# Return Value
		return Value
	
	# Instant Battery Capacity Validator
	@validator('B_IC', pre=True, always=True)
	def B_IC_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 10000:

			# Raise Error
			raise ValueError(f"Invalid instant battery capacity. Expected '0 - 10000', got {Value}")

		# Return Value
		return Value
	
	# Battery State of Charge Validator
	@validator('B_SOC', pre=True, always=True)
	def B_SOC_Validator(cls, Value):

		# Check Value
		if not 0.0 <= Value <= 100.0:

			# Raise Error
			raise ValueError(f"Invalid battery state of charge. Expected '0.0 - 100.0', got {Value}")

		# Return Value
		return Value
	
	# Battery Temperature Validator
	@validator('B_T', pre=True, always=True)
	def B_T_Validator(cls, Value):

		# Check Value
		if not -50.0 <= Value <= 100.0:

			# Raise Error
			raise ValueError(f"Invalid battery temperature. Expected '-50.0 - 100.0', got {Value}")

		# Return Value
		return Value
	
	# Battery Charge State Validator
	@validator('B_CS', pre=True, always=True)
	def B_CS_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 5:

			# Raise Error
			raise ValueError(f"Invalid battery charge state. Expected '0 - 5', got {Value}")

		# Return Value
		return Value

# Define IoT 
class IoT(BaseModel):

	# GSM Module Firmware
	Firmware: Optional[str] = Field(description="Modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(description="GSM modem IMEI number.", example="356156060000000", min_length=10, max_length=15)

	# SIM ICCID
	ICCID: str = Field(description="SIM card ICCID number.", example="8990011916180280000", min_length=10, max_length=20)

	# RSSI
	RSSI: Optional[int] = Field(description="IoT RSSI signal level.", example=28, min=-100, max=100)

	# Connection Time
	ConnTime: Optional[int] = Field(description="IoT connection time.", example=12, min=0, max=100000)

	# TAC
	TAC: Optional[int] = Field(description="Operator type allocation code.", example=34124, min=0, max=65535)

	# LAC
	LAC: Optional[int] = Field(description="Operator base station location.", example=34124, min=0, max=65535)

	# Cell ID
	Cell_ID: Optional[int] = Field(description="Operator base station cell id.", example=34124, min=0, max=65535)

	# Firmware Validator
	@validator('Firmware', pre=True, always=True)
	def Version_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{3}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid version format. Expected 'XX.XX.XXX', got {Value}")

		# Return Value
		return Value

	# IMEI Validator
	@validator('IMEI', pre=True, always=True)
	def IMEI_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{10,15}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid IMEI format. Expected 'XXXXXXXXXXXXXXX', got {Value}")

		# Return Value
		return Value
	
	# ICCID Validator
	@validator('ICCID', pre=True, always=True)
	def ICCID_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{10,20}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid ICCID format. Expected 'XXXXXXXXXXXXXXXXXXXX', got {Value}")

		# Return Value
		return Value

	# RSSI Validator
	@validator('RSSI', pre=True, always=True)
	def RSSI_Validator(cls, Value):

		# Check Value
		if not -100 <= Value <= 100:

			# Raise Error
			raise ValueError(f"Invalid RSSI format. Expected '-100 - 100', got {Value}")

		# Return Value
		return Value

	# Connection Time Validator
	@validator('ConnTime', pre=True, always=True)
	def ConnTime_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 100000:

			# Raise Error
			raise ValueError(f"Invalid connection time format. Expected '0 - 100000', got {Value}")

		# Return Value
		return Value

	# TAC Validator
	@validator('TAC', pre=True, always=True)
	def TAC_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 65535:

			# Raise Error
			raise ValueError(f"Invalid TAC format. Expected '0 - 65535', got {Value}")

		# Return Value
		return Value
	
	# LAC Validator
	@validator('LAC', pre=True, always=True)
	def LAC_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 65535:

			# Raise Error
			raise ValueError(f"Invalid LAC format. Expected '0 - 65535', got {Value}")

		# Return Value
		return Value
	
	# Cell ID Validator
	@validator('Cell_ID', pre=True, always=True)
	def Cell_ID_Validator(cls, Value):

		# Check Value
		if not 0 <= Value <= 65535:

			# Raise Error
			raise ValueError(f"Invalid cell ID format. Expected '0 - 65535', got {Value}")

		# Return Value
		return Value

# Define Device
class Device(BaseModel):
    
	# Device Power
	Power: Power

	# Device IoT
	IoT: IoT

# Define payload
class WeatherStat_Payload(BaseModel):

	# Latitude Value of Device
	Latitude: Optional[float] = Field(description="GNSS lattitude value.", example=1.243242342, min=-360, max=360)

	# Longtitude Value of Device
	Longtitude: Optional[float] = Field(description="GNSS longtitude value.", example=23.3213232, min=-360, max=360)
    
	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(description="Air temperature.", example=28.3232, min=-50.0, max=100.0)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(description="Air humidity.", example=85.2332, min=0.0, max=100.0)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(description="Air pressure.", example=985.55, min=500.0, max=2000.0)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(description="Visual light.", example=1234, min=0, max=100000)

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(description="Infrared light.", example=1234, min=0, max=100000)

	# Last Measured UV Value
	UV: Optional[float] = Field(description="UV index.", example=2.12, min=0.0, max=20.0)

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=0, max_items=10, min=-50.0, max=100.0)

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23, min=0, max=100000)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275, min=0, max=360)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25, min=0.0, max=100.0)

# Define IoT RAW Data Base Model
# WeatherStat Model Version 01.03.00
class Data_Pack(BaseModel):

	# Info
	Info: Info

	# Device
	Device: Device

	# Payload
	Payload: WeatherStat_Payload
