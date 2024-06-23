# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from Setup.Definitions import Constants
from Setup import Models, Database
from Functions import Log
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Annotated, Type, Dict, Tuple, Any
from datetime import datetime
import re

# Define IoT Data Base Model

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
		default=Constants.INFO.DEFAULT_COMMAND,
		json_schema_extra={
			"examples": Constants.INFO.COMMAND_ALLOWED,
			"min_length": Constants.INFO.COMMAND_MIN_LENGTH,
			"max_length": Constants.INFO.COMMAND_MAX_LENGTH
		}
	)]

	# Command Validator
	@field_validator("Command", mode='before')
	def validate_command(cls, value: str) -> str:

		# Check Command
		if value not in Constants.INFO.COMMAND_ALLOWED:

			# Set Default Value
			return Constants.INFO.DEFAULT_COMMAND

		# Return Command
		return value

	# Timestamp
	TimeStamp: Annotated[str, Field(
		description="Measurement time stamp.",
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
		default=Constants.INFO.DEFAULT_ID,
		json_schema_extra={
			"example": "8B00000000000000"
		}
	)]

	# Device ID Validator
	@field_validator('ID', mode='before')
	def validate_id(cls, value: str) -> str:

		# Check ID
		if not re.match(Constants.INFO.ID_PATTERN, value):

			# Set Default Value
			return Constants.INFO.DEFAULT_ID

		# Return ID
		return value

	# Device Firmware Version
	Firmware: Annotated[Optional[str], Field(
		description="Firmware version of device.",
		default=Constants.INFO.DEFAULT_FIRMWARE,
		json_schema_extra={
			"example": "01.00.00",
			"pattern": Constants.INFO.FIRMWARE_PATTERN
		}
	)]

	# Firmware Validator
	@field_validator('Firmware', mode='before')
	def validate_firmware(cls, value: Optional[str]) -> str:

		# Check Value
		if value is None or not re.match(Constants.INFO.FIRMWARE_PATTERN, value):

			# Set Default Value
			return Constants.INFO.DEFAULT_FIRMWARE

		# Return Value
		return value

# Define Power
class Power(CustomBaseModel):

	# Instant Battery Voltage
	B_IV: Annotated[float, Field(
		description="Battery instant voltage.",
		json_schema_extra={
			"example": 3.8,
			"minimum": Constants.BATTERY.VOLTAGE_MIN,
			"maximum": Constants.BATTERY.VOLTAGE_MAX
		},
        ge=Constants.BATTERY.VOLTAGE_MIN,
        le=Constants.BATTERY.VOLTAGE_MAX		
	)]

	# Battery Instant Voltage Validator
	@field_validator('B_IV', mode='before')
	def validate_b_iv(cls, value: float) -> float:

		# Check Value
		if value is None or not Constants.BATTERY.VOLTAGE_MIN <= value <= Constants.BATTERY.VOLTAGE_MAX:

			# Raise Error
			raise ValueError(f"B_IV must be between {Constants.BATTERY.VOLTAGE_MIN} and {Constants.BATTERY.VOLTAGE_MAX}")

		# Return Value
		return value

	# Average Battery Current
	B_AC: Annotated[float, Field(
		description="Battery average current.",
		json_schema_extra={
			"example": 0.2,
			"minimum": Constants.BATTERY.CURRENT_MIN,
			"maximum": Constants.BATTERY.CURRENT_MAX
		},
        ge=Constants.BATTERY.CURRENT_MIN,
        le=Constants.BATTERY.CURRENT_MAX		
	)]

	# Battery Average Current Validator
	@field_validator('B_AC', mode='before')
	def validate_b_ac(cls, value: float) -> float:

		# Check Value
		if value is None or not Constants.BATTERY.CURRENT_MIN <= value <= Constants.BATTERY.CURRENT_MAX:

			# Raise Error
			raise ValueError(f"B_AC must be between {Constants.BATTERY.CURRENT_MIN} and {Constants.BATTERY.CURRENT_MAX}")

		# Return Value
		return value

	# Full Battery Capacity
	B_FC: Annotated[Optional[int], Field(
		description="Full battery capacity.",
		default=None,
		json_schema_extra={
			"example": 2000,
			"minimum": Constants.BATTERY.CAPACITY_MIN,
			"maximum": Constants.BATTERY.CAPACITY_MAX
		},
        ge=Constants.BATTERY.CAPACITY_MIN,
        le=Constants.BATTERY.CAPACITY_MAX
	)]

	# Full Battery Capacity Validator
	@field_validator('B_FC', mode='before')
	def validate_b_fc(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and not Constants.BATTERY.CAPACITY_MIN <= value <= Constants.BATTERY.CAPACITY_MAX:

			# Set Default Value
			return Constants.BATTERY.DEFAULT_CAPACITY

		# Return Value
		return value

	# Instant Battery Capacity
	B_IC: Annotated[Optional[int], Field(
		description="Instant battery capacity.",
		default=None,
		json_schema_extra={
			"example": 1820,
			"minimum": Constants.BATTERY.INSTANT_CAPACITY_MIN,
			"maximum": Constants.BATTERY.INSTANT_CAPACITY_MAX
		},
		ge=Constants.BATTERY.INSTANT_CAPACITY_MIN,
		le=Constants.BATTERY.INSTANT_CAPACITY_MAX
	)]

	# Instant Battery Capacity Validator
	@field_validator('B_IC', mode='before')
	def validate_b_ic(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and not Constants.BATTERY.INSTANT_CAPACITY_MIN <= value <= Constants.BATTERY.INSTANT_CAPACITY_MAX:

			# Set Default Value
			return Constants.BATTERY.DEFAULT_INSTANT_CAPACITY

		# Return Value
		return value

	# Battery State of Charge
	B_SOC: Annotated[Optional[float], Field(
		description="Battery state of charge.",
		default=None,
		json_schema_extra={
			"example": 97.30,
			"minimum": Constants.BATTERY.SOC_MIN,
			"maximum": Constants.BATTERY.SOC_MAX
		},
		ge=Constants.BATTERY.SOC_MIN,
		le=Constants.BATTERY.SOC_MAX
	)]

	# Battery State of Charge Validator
	@field_validator('B_SOC', mode='before')
	def validate_b_soc(cls, value: Optional[float]) -> Optional[float]:

		# Check Value
		if value is None or not Constants.BATTERY.SOC_MIN <= value <= Constants.BATTERY.SOC_MAX:

			# Set Default Value
			return Constants.BATTERY.DEFAULT_SOC

		# Return Value
		return value

	# Battery Temperature
	B_T: Annotated[Optional[float], Field(
		description="Battery temperature.",
		default=None,
		json_schema_extra={
			"example": 32.1903,
			"minimum": Constants.BATTERY.TEMPERATURE_MIN,
			"maximum": Constants.BATTERY.TEMPERATURE_MAX
		},
		ge=Constants.BATTERY.TEMPERATURE_MIN,
		le=Constants.BATTERY.TEMPERATURE_MAX
	)]

	# Battery Temperature Validator
	@field_validator('B_T', mode='before')
	def validate_b_t(cls, value: Optional[float]) -> Optional[float]:

		# Check Value
		if value is not None and not Constants.BATTERY.TEMPERATURE_MIN <= value <= Constants.BATTERY.TEMPERATURE_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_TEMPERATURE

		# Return Value
		return value

	B_CS: Constants.BATTERY.CHARGE_STATE = Field(
		description="Battery charge state.",
		default=Constants.BATTERY.CHARGE_STATE.UNKNOWN,
		json_schema_extra={
			"examples": [Constants.BATTERY.CHARGE_STATE.UNKNOWN]
		}
	)

	# Battery Charge State Validator
	@field_validator('B_CS', mode='before')
	def validate_b_charge_state(cls, value: Optional[int]) -> Optional[int]:

		# Convert integer to corresponding Enum value
		if isinstance(value, int):

			# Convert to Enum
			value = Constants.BATTERY.CHARGE_STATE(value)

		# Check Value
		elif not isinstance(value, Constants.BATTERY.CHARGE_STATE):

			# If value is not valid, set to default
			value = Constants.BATTERY.CHARGE_STATE.UNKNOWN

		# Return Value
		return value

# Define IoT
class IoT(CustomBaseModel):

	# GSM Module Firmware
	Firmware: Annotated[Optional[str], Field(
		description="Modem firmware version.",
		default=None,
		json_schema_extra={
			"example": "13.00.007",
			"pattern": Constants.IOT.FIRMWARE_PATTERN 
		}
	)]

	# Firmware Validator
	@field_validator('Firmware', mode='before')
	def validate_firmware(cls, value: Optional[str]) -> Optional[str]:

		# Check Value
		if value is None or not re.match(Constants.IOT.FIRMWARE_PATTERN, value):

			# Set Default Value
			return Constants.IOT.DEFAULT_FIRMWARE

		# Return Value
		return value

	# Module IMEI Number
	IMEI: Annotated[Optional[str], Field(
		description="GSM modem IMEI number.",
		default=None,
		json_schema_extra={
			"example": "356156060000000",
			"min_length": Constants.IOT.IMEI_MIN_LENGTH,
			"max_length": Constants.IOT.IMEI_MAX_LENGTH,
			"pattern": Constants.IOT.IMEI_PATTERN
		}
	)]

	# IMEI Validator
	@field_validator('IMEI', mode='before')
	def validate_imei(cls, value: Optional[str]) -> Optional[str]:

		# Check Value
		if value is None or not re.match(Constants.IOT.IMEI_PATTERN, value):

			# Set Default Value
			value = Constants.IOT.DEFAULT_IMEI

		# Return Value
		return value

	# SIM ICCID
	ICCID: Annotated[str, Field(
		description="SIM card ICCID number.",
		default=Constants.IOT.DEFAULT_ICCID,
		json_schema_extra={
			"example": "8990011916180280000",
			"min_length": Constants.IOT.ICCID_MIN_LENGTH,
			"max_length": Constants.IOT.ICCID_MAX_LENGTH,
			"pattern": Constants.IOT.ICCID_PATTERN 
		}
	)]

	# ICCID Validator
	@field_validator('ICCID', mode='before')
	def validate_iccid(cls, value: str) -> str:

		# Check Value
		if value is None or not re.match(Constants.IOT.ICCID_PATTERN, value):

			# Set Default Value
			return Constants.IOT.DEFAULT_ICCID

		# Return Value
		return value

	# RSSI
	RSSI: Annotated[Optional[int], Field(
		description="IoT RSSI signal level.",
		default=None,
		json_schema_extra={
			"example": 28,
			"minimum": Constants.IOT.RSSI_MIN,
			"maximum": Constants.IOT.RSSI_MAX
		},
		ge=Constants.IOT.RSSI_MIN,
		le=Constants.IOT.RSSI_MAX
	)]

	# RSSI Validator
	@field_validator('RSSI', mode='before')
	def validate_rssi(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and (value <= Constants.IOT.RSSI_MIN or value >= Constants.IOT.RSSI_MAX):

			# Set Default Value
			return Constants.IOT.DEFAULT_RSSI

		# Return Value
		return value

	# Connection Time
	ConnTime: Annotated[Optional[float], Field(
		description="IoT connection time.",
		default=None,
		json_schema_extra={
			"example": 1.32,
			"minimum": Constants.IOT.CONNECTION_TIME_MIN,
			"maximum": Constants.IOT.CONNECTION_TIME_MAX
		},
		ge=Constants.IOT.CONNECTION_TIME_MIN,
		le=Constants.IOT.CONNECTION_TIME_MAX
	)]

	# Connection Time Validator
	@field_validator('ConnTime', mode='before')
	def validate_conn_time(cls, value: Optional[float]) -> Optional[float]:

		# Check Value
		if value is not None and (value < Constants.IOT.CONNECTION_TIME_MIN or value > Constants.IOT.CONNECTION_TIME_MAX):

			# Set Default Value
			return Constants.IOT.DEFAULT_CONNECTION_TIME

		# Return Value
		return value

	# MCC
	MCC: Annotated[Optional[int], Field(
		description="Mobile country code.",
		default=286, # Turkey
		json_schema_extra={
			"example": 286
		}
	)]

	# MNC
	MNC: Annotated[Optional[int], Field(
		description="Mobile network code.",
		default=1, # Turkcell
		json_schema_extra={
			"example": 1
		}
	)]

	# TAC
	TAC: Annotated[Optional[int], Field(
		description="Operator type allocation code.",
		default=None,
		json_schema_extra={
			"example": 34124,
			"minimum": Constants.IOT.TAC_MIN,
			"maximum": Constants.IOT.TAC_MAX
		},
		ge=Constants.IOT.TAC_MIN,
		le=Constants.IOT.TAC_MAX
	)]

	# TAC Validator
	@field_validator("TAC", mode='before')
	def validate_tac(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and (value < Constants.IOT.TAC_MIN or value > Constants.IOT.TAC_MAX):

			# Set Default Value
			return Constants.IOT.DEFAULT_TAC

		# Return Value
		return value

	# LAC
	LAC: Annotated[Optional[int], Field(
		description="Operator base station location.",
		default=None,
		json_schema_extra={
			"example": 34124,
			"minimum": Constants.IOT.LAC_MIN,
			"maximum": Constants.IOT.LAC_MAX
		},
		ge=Constants.IOT.LAC_MIN,
		le=Constants.IOT.LAC_MAX
	)]

	# LAC Validator
	@field_validator("LAC", mode='before')
	def validate_lac(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and (value < Constants.IOT.LAC_MIN or value > Constants.IOT.LAC_MAX):

			# Set Default Value
			return Constants.IOT.DEFAULT_LAC

		# Return Value
		return value

	# Cell ID
	Cell_ID: Annotated[Optional[int], Field(
		description="Operator base station cell ID.",
		default=None,
		json_schema_extra={
			"example": 34124,
			"minimum": Constants.IOT.CELL_ID_MIN,
			"maximum": Constants.IOT.CELL_ID_MAX
		},
		ge=Constants.IOT.CELL_ID_MIN,
		le=Constants.IOT.CELL_ID_MAX
	)]

	# Cell ID Validator
	@field_validator("Cell_ID", mode='before')
	def validate_cell_id(cls, value: Optional[int]) -> Optional[int]:

		# Check Value
		if value is not None and (value < Constants.IOT.CELL_ID_MIN or value > Constants.IOT.CELL_ID_MAX):

			# Set Default Value
			return Constants.IOT.DEFAULT_CELL_ID

		# Return Value
		return value

	# WDS
	WDS: Annotated[Constants.IOT.WDS, Field(
		description="IoT WDS type.",
		default=None,
		json_schema_extra={
			"example": Constants.IOT.WDS.CONNECTION_4G
		}
	)]

	# WDS Validator
	@field_validator('WDS', mode='before')
	def validate_wds(cls, value: Optional[int]) -> Optional[int]:

		# Convert integer to corresponding Enum value
		if isinstance(value, int):

			# Convert to Enum
			return Constants.IOT.WDS(value)

		# Check Value
		else:

			# If value is not valid, set to default
			return Constants.IOT.WDS.UNKNOWN

# Define Device
class Device(CustomBaseModel):

	# Device Power
	Power: Power

	# Device IoT
	IoT: IoT

# Dynamic Payload Model Creator
def Create_Dynamic_Payload_Model():

	attributes: Dict[str, Any] = {}

	try:
		with Database.DB_Session_Scope() as DB:
			query_variables = DB.query(Models.Variable).all()

			for variable in query_variables:
				# Specify the field type and additional properties directly
				attributes[variable.Variable_ID] = (Optional[float], Field(
					default=None, 
					description=variable.Variable_Description,
					ge=variable.Variable_Min_Value if variable.Variable_Min_Value is not None else None,
					le=variable.Variable_Max_Value if variable.Variable_Max_Value is not None else None
				))

		# Create and return the dynamic Pydantic model class
		return type('DynamicModel', (CustomBaseModel,), attributes)

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Raise Error
		raise RuntimeError(f"Failed to create dynamic model due to database error: {str(e)}") from e

	# Handle Exceptions
	except Exception as e:

		# Raise Error
		raise RuntimeError(f"An unexpected error occurred while creating the dynamic model: {str(e)}") from e

# Define Payload payload
#Dynamic_Payload = Create_Dynamic_Payload_Model()

# Define IoT RAW Data Base Model
class Data_Pack(CustomBaseModel):

	# Info
	Info: Info

	# Device
	Device: Device

	# Payload
#	Payload: Dynamic_Payload
