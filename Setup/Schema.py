# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from Setup.Definitions import Variable_Segment as Constants
from Setup.Definitions import Constants as Default

from Functions import Database_Functions
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime
import re

# Custom Base Model
class CustomBaseModel(BaseModel):
	def model_dump(self, **kwargs):
		kwargs['exclude_none'] = True
		return super().model_dump(**kwargs)
	class Config:
		extra = 'ignore'

# Define Info
class Info(CustomBaseModel):

	# Define Command
	Command: Annotated[str, Field(
		description="Pack command.",
		default=Default.INFO.DEFAULT_COMMAND,
		json_schema_extra={
			"examples": Default.INFO.COMMAND_ALLOWED,
			"min_length": Default.INFO.COMMAND_MIN_LENGTH,
			"max_length": Default.INFO.COMMAND_MAX_LENGTH
		}
	)]

	# Command Validator
	@field_validator("Command", mode='before')
	def validate_command(cls, value: str) -> str:

		# Check Command
		if value not in Default.INFO.COMMAND_ALLOWED:

			# Set Default Value
			return Default.INFO.DEFAULT_COMMAND

		# Return Command
		return value

	# Timestamp
	TimeStamp: Annotated[str, Field(
		description="Measurement time stamp.",
		default="2024-01-01T00:00:00",
		json_schema_extra={
			"example": "2023-10-29T08:28:32"
		}
	)]

	# Timestamp Validator
	@field_validator('TimeStamp', mode='before')
	def validate_timestamp(cls, value: str) -> str:

		# Try to parse the timestamp
		try:

			# Check if 'Z' is in the value
			if 'Z' in value:

				# Replace 'Z' with '+00:00'
				value = value.replace('Z', '+00:00')

			# Check if there is a timezone offset
			value = re.sub(r'\+\d{2}:\d{2}', '', value)

			# Parse the timestamp
			parsed_timestamp = datetime.fromisoformat(value)

			# Return the formatted timestamp
			return parsed_timestamp.strftime('%Y-%m-%dT%H:%M:%S')

		# If the value is not a valid timestamp
		except ValueError:

			# Return the default timestamp
			return "2024-01-01T00:00:00"

	# Device ID
	ID: Annotated[str, Field(
		description="IoT device unique ID.",
		default=Default.INFO.DEFAULT_ID,
		json_schema_extra={
			"example": "8B00000000000000"
		}
	)]

	# Device ID Validator
	@field_validator('ID', mode='before')
	def validate_id(cls, value: str) -> str:

		# Check ID
		if not re.match(Default.INFO.ID_PATTERN, value):

			# Set Default Value
			return Default.INFO.DEFAULT_ID

		# Return ID
		return value

	# Module IMEI Number
	IMEI: Annotated[Optional[str], Field(
		description="GSM modem IMEI number.",
		default=None,
		json_schema_extra={
			"example": "356156060000000",
			"min_length": Default.IOT.IMEI_MIN_LENGTH,
			"max_length": Default.IOT.IMEI_MAX_LENGTH,
			"pattern": Default.IOT.IMEI_PATTERN
		}
	)]

	# IMEI Validator
	@field_validator('IMEI', mode='before')
	def validate_imei(cls, value: Optional[str]) -> Optional[str]:

		# Check Value
		if value is None or not re.match(Default.IOT.IMEI_PATTERN, value):

			# Set Default Value
			value = Default.IOT.DEFAULT_IMEI

		# Return Value
		return value

	# SIM ICCID
	ICCID: Annotated[str, Field(
		description="SIM card ICCID number.",
		default=Default.IOT.DEFAULT_ICCID,
		json_schema_extra={
			"example": "8990011916180280000",
			"min_length": Default.IOT.ICCID_MIN_LENGTH,
			"max_length": Default.IOT.ICCID_MAX_LENGTH,
			"pattern": Default.IOT.ICCID_PATTERN 
		}
	)]

	# ICCID Validator
	@field_validator('ICCID', mode='before')
	def validate_iccid(cls, value: str) -> str:

		# Check Value
		if value is None or not re.match(Default.IOT.ICCID_PATTERN, value):

			# Set Default Value
			return Default.IOT.DEFAULT_ICCID

		# Return Value
		return value

	# Device Firmware Version
	Firmware: Annotated[Optional[str], Field(
		description="Firmware version of device.",
		default=Default.INFO.DEFAULT_FIRMWARE,
		json_schema_extra={
			"example": "01.00.00",
			"pattern": Default.INFO.FIRMWARE_PATTERN
		}
	)]

	# Firmware Validator
	@field_validator('Firmware', mode='before')
	def validate_firmware(cls, value: Optional[str]) -> str:

		# Check Value
		if value is None or not re.match(Default.INFO.FIRMWARE_PATTERN, value):

			# Set Default Value
			return Default.INFO.DEFAULT_FIRMWARE

		# Return Value
		return value

# Define Device Power Model
Dynamic_Power = Database_Functions.Create_Dynamic_Model(Constants.Power.value)

# Define Device IoT Model
Dynamic_IoT = Database_Functions.Create_Dynamic_Model(Constants.GSM.value)

# Define Device
class Device(CustomBaseModel):

	# Device Power
	Power: Optional[Dynamic_Power]

	# Device IoT
	IoT: Optional[Dynamic_IoT]

# Define Payload payload
Dynamic_Payload = Database_Functions.Create_Dynamic_Model(Constants.Unknown.value)

# Define IoT RAW Data Base Model
class Data_Pack(CustomBaseModel):

	# Info
	Info: Optional[Info]

	# Device
	Device: Optional[Device]

	# Payload
	Payload: Optional[Dynamic_Payload]

# Define Response Model
class Service_Response(CustomBaseModel):

	# Define Response
	Event: Annotated[int, Field(
		description="Response event code.",
		json_schema_extra={
			"example": 200
		}
	)]