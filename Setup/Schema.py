# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, field_validator, root_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional, Dict, List
import re, ipaddress
from datetime import datetime

# Define Field Validator
def Field_Alias(Values: Dict, Field_Alias_List: str, Aliases: List[str], Optional: bool = False) -> Dict:
    
	# Check if normalized_name is in values
	for Alias in Aliases:

		# Check if alias is in values
		if Alias in Values:

			# Control for Optional and None
			if Optional and Values[Alias] is None:
				continue

			# Set normalized_name
			Values[Field_Alias_List] = Values[Alias]
            
			# Break
			break
	
	# Return Values
	return Values

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

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "ID", ["ID", "id", "Id"])
		Field_Alias(values, "Hardware", ["HARDWARE", "Hardware", "HardWare", "hardware", "HW", "hw", "Hw"], Optional=True)
		Field_Alias(values, "Firmware", ["FIRMWARE", "Firmware", "FirmWare", "firmware", "FW", "fw", "Fw"], Optional=True)

		# Return values
		return values

	# Device ID Validator
	@field_validator('ID')
	@classmethod
	def ID_Validator(cls, ID_Value):

		# Define Regex Pattern
		Pattern = r'^[0-9A-F]{10,16}$'

		# Check ID
		if not re.match(Pattern, ID_Value):

			# Raise Error
			raise ValueError(f"Invalid ID format. Expected 'XXXXXXXXXXXXXXXX', got {ID_Value}")

		# Return ID
		return ID_Value

	# Hardware and Firmware Validator
	@field_validator('Hardware', 'Firmware')
	@classmethod
	def Version_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid version format. Expected 'XX.XX.XX', got {Value}")

		# Return Value
		return Value

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

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "IV", ["IV", "iv", "Iv"])
		Field_Alias(values, "AC", ["AC", "ac", "Ac"])
		Field_Alias(values, "SOC", ["SOC", "soc", "Soc"])
		Field_Alias(values, "T", ["T", "t"], Optional=True)
		Field_Alias(values, "FB", ["FB", "fb", "Fb"], Optional=True)
		Field_Alias(values, "IB", ["IB", "ib", "Ib"], Optional=True)
		Field_Alias(values, "Charge", ["CHARGE", "Charge", "charge"])

		# Return values
		return values

	# Charge Validator
	@field_validator("Charge")
	@classmethod
	def Validate_Charge(cls, value):

		# Check Charge
		if value < 0 or value > 5:
			
			# Set Value
			return 5

		# Return Value
		return value

# Define Power
class Pack_Power(BaseModel):

	# Device Battery
	Battery: Pack_Battery

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Battery", ["BATTERY", "Battery", "battery", "BAT", "Bat", "bat"])

		# Return values
		return values

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

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Firmware", ["FIRMWARE", "Firmware", "firmware", "FW", "fw", "Fw"], Optional=True)
		Field_Alias(values, "IMEI", ["IMEI", "Imei", "imei"], Optional=True)
		Field_Alias(values, "Manufacturer", ["MANUFACTURER", "Manufacturer", "Man", "man", "MF"], Optional=True)
		Field_Alias(values, "Model", ["MODEL", "Model", "model", "MD"], Optional=True)
		Field_Alias(values, "Serial", ["SERIAL", "Serial", "serial", "SR"], Optional=True)

		# Return values
		return values

	# Firmware Validator
	@field_validator('Firmware')
	@classmethod
	def Version_Validator(cls, Value):

		# Define Regex Pattern
		Pattern = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2,3}$'

		# Check Value
		if not re.match(Pattern, Value):

			# Raise Error
			raise ValueError(f"Invalid version format. Expected 'XX.XX.XX', got {Value}")

		# Return Value
		return Value

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

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:
		
		# Set Alias Alternatives
		Field_Alias(values, "SIM_Type", ["SIM_TYPE", "Sim_Type", "sim_type", "SIMTYPE", "SimType", "simtype", "SIM", "Sim", "sim"], Optional=True)
		Field_Alias(values, "ICCID", ["ICCID", "Iccid", "iccid"])
		Field_Alias(values, "MCC", ["MCC", "Mcc", "mcc"], Optional=True)
		Field_Alias(values, "MNC", ["MNC", "Mnc", "mnc"], Optional=True)
		Field_Alias(values, "RSSI", ["RSSI", "Rssi", "rssi", "DBM", "dBm", "dbm"], Optional=True)
		Field_Alias(values, "TAC", ["TAC", "Tac", "tac"], Optional=True)
		Field_Alias(values, "LAC", ["LAC", "Lac", "lac"], Optional=True)
		Field_Alias(values, "Cell_ID", ["CELL_ID", "Cell_Id", "cell_id", "CELLID", "CellId", "cellid"], Optional=True)
		Field_Alias(values, "IP", ["IP", "Ip", "ip"], Optional=True)
		Field_Alias(values, "ConnTime", ["CONNTIME", "ConnTime", "conntime", "CONNECTION_TIME", "Connection_Time", "connection_time", "CONNECTIONTIME", "ConnectionTime", "connectiontime"], Optional=True)

		# Return values
		return values

	# IP Validator
	@field_validator("IP")
	@classmethod
	def Validate_IP(cls, value):

		# Check IP
		if value is not None:

			# Check IP
			try:

				# Convert to IP
				ipaddress.ip_address(value)

			except ValueError:

				# Set IP
				value = "0.0.0.0"

# Define GSM
class Pack_GSM(BaseModel):

	# Device IoT Module
	Module: Optional[Pack_IoT_Module]

	# IoT Operator
	Operator: Pack_IoT_Operator

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Module", ["MODULE", "Module", "module", "MD", "md", "Md"], Optional=True)
		Field_Alias(values, "Operator", ["OPERATOR", "Operator", "operator", "OP", "op", "Op"])

		# Return values
		return values

# Define IoT
class Pack_IoT(BaseModel):
	
	# Device GSM
	GSM: Pack_GSM

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "GSM", ["GSM", "Gsm", "gsm"])

		# Return values
		return values

# Define Device
class Pack_Device(BaseModel):

	# Device Info
	Info: Pack_Info

	# Device Power
	Power: Pack_Power

	# Device IoT
	IoT: Pack_IoT

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Info", ["INFO", "Info", "info"])
		Field_Alias(values, "Power", ["POWER", "Power", "power", "POW", "Pow", "pow"])
		Field_Alias(values, "IoT", ["IOT", "Iot", "iot"])

		# Return values
		return values

# Location Definition
class Payload_WeatherStat_Location(BaseModel):

	# Latitude Value of Device
	Latitude: float = Field(description="GNSS lattitude value.", example=1.243242342)

	# Longtitude Value of Device
	Longtitude: float = Field(description="GNSS longtitude value.", example=23.3213232)

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Latitude", ["LATITUDE", "Latitude", "latitude", "LAT", "Lat", "lat"])
		Field_Alias(values, "Longtitude", ["LONGTITUDE", "Longtitude", "longtitude", "LONG", "Long", "long", "Longitude", "longitude", "LONGITUDE"])

		# Return values
		return values

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

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "AT", ["AT", "at", "At"], Optional=True)
		Field_Alias(values, "AH", ["AH", "ah", "Ah"], Optional=True)
		Field_Alias(values, "AP", ["AP", "ap", "Ap"], Optional=True)
		Field_Alias(values, "UV", ["UV", "uv", "Uv"], Optional=True)
		Field_Alias(values, "VL", ["VL", "vl", "Vl"], Optional=True)
		Field_Alias(values, "IL", ["IL", "il", "Il"], Optional=True)
		Field_Alias(values, "ST", ["ST", "st", "St"], Optional=True)
		Field_Alias(values, "R", ["R", "r", "Rain", "rain", "RAIN"], Optional=True)
		Field_Alias(values, "WS", ["WS", "ws", "Ws", "WindSpeed", "windspeed", "WINDSPEED"], Optional=True)
		Field_Alias(values, "WD", ["WD", "wd", "Wd", "WindDirection", "winddirection", "WINDDIRECTION"], Optional=True)

		# Return values
		return values

# WeatherStat Model Definition
class Payload_WeatherStat(BaseModel):

	# Location
	Location: Optional[Payload_WeatherStat_Location]

	# Environment
	Environment: Payload_WeatherStat_Environment

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Location", ["LOCATION", "Location", "location", "LOC", "Loc", "loc"], Optional=True)
		Field_Alias(values, "Environment", ["ENVIRONMENT", "Environment", "environment", "ENV", "Env", "env"])

		# Return values
		return values

# Define payload
class Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(description="Measurement time stamp.", example="2022-07-19T08:28:32Z")

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat]

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "TimeStamp", ["TIMESTAMP", "TimeStamp", "timestamp", "TIME", "Time", "time", "TS", "Ts", "ts"])
		Field_Alias(values, "WeatherStat", ["WEATHERSTAT", "WeatherStat", "weatherstat", "WEATHER", "Weather", "weather", "WS", "Ws", "ws"], Optional=True)

		# Return values
		return values

    # TimeStamp Validator
	@field_validator('TimeStamp')
	@classmethod
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

# Define IoT RAW Data Base Model
# WeatherStat Model Version 01.03.00
class Data_Pack_Model(BaseModel):

	# Define Command
	Command: str = Field(description="Pack command.", example="Demo:PowerStat.Online")

	# Device
	Device: Optional[Pack_Device]

	# Payload
	Payload: Payload

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Field_Alias(values, "Command", ["COMMAND", "Command", "command", "CMD", "Cmd", "cmd"])
		Field_Alias(values, "Device", ["DEVICE", "Device", "device", "DEV", "Dev", "dev"], Optional=True)
		Field_Alias(values, "Payload", ["PAYLOAD", "Payload", "payload", "PAY", "Pay", "pay"])

		# Return values
		return values

	# Command Validator
	@field_validator('Command')
	@classmethod
	def Command_Validator(cls, Command_Value):

		# Define Regex Pattern
		pattern = r'^[a-zA-Z]+:[a-zA-Z]+\.[a-zA-Z]+$'
        
		# Check Command
		if not re.match(pattern, Command_Value, re.IGNORECASE):

			# Raise Error
			raise ValueError(f"Invalid command format. Expected 'xxx:yyy.zzz', got {Command_Value}")

		# Return Command
		return Command_Value.upper()
