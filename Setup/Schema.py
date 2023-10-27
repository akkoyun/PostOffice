# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, field_validator, root_validator
from typing import Optional, Dict
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

	# Handle ID Field Name
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:
		
		# Set Alias Alternatives
		Alias_Alternatives_ID = ["ID", "id", "Id"]
		Alias_Alternatives_Hardware = ["HARDWARE", "Hardware", "HardWare", "hardware", "HW", "hw", "Hw"]
		Alias_Alternatives_Firmware = ["FIRMWARE", "Firmware", "FirmWare", "firmware", "FW", "fw", "Fw"]

		# Normalize ID Field
		for Alias in Alias_Alternatives_ID:

			# Check ID Field
			if Alias in values:
				
				# Set ID Field
				values["ID"] = values[Alias]

				# Break
				break

		# Normalize Hardware Field
		for Alias in Alias_Alternatives_Hardware:

			# Check Hardware Field
			if Alias in values:
				
				# Set Hardware Field
				values["Hardware"] = values[Alias]

				# Break
				break

		# Normalize Firmware Field
		for Alias in Alias_Alternatives_Firmware:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["Firmware"] = values[Alias]

				# Break
				break

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
	AC: float = Field(description="Battery average current.", example=0.2, min=-10000, max=10000)

	# Battery State of Charge
	SOC: float = Field(description="Battery state of charge.", example=97.30, min=0.0, max=100.0)

	# Battery Temperature
	T: Optional[float] = Field(default=None, description="Battery temperature.", example=32.1903, min=-50.0, max=100.0)

	# Battery Full Battery Cap
	FB: Optional[int] = Field(default=None, description="Full battery capacity.", example=2000, min=0, max=10000)

	# Battery Instant Battery Cap
	IB: Optional[int] = Field(default=None, description="Instant battery capacity.", example=1820, min=0, max=10000)

	# Battery Charge State
	Charge: int = Field(description="Battery charge state.", example=1, min=0, max=5)

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:
		
		# Set Alias Alternatives
		Alias_Alternatives_IV = ["IV", "iv", "Iv"]
		Alias_Alternatives_AC = ["AC", "ac", "Ac"]
		Alias_Alternatives_SOC = ["SOC", "soc", "Soc"]
		Alias_Alternatives_T = ["T", "t"]
		Alias_Alternatives_FB = ["FB", "fb", "Fb"]
		Alias_Alternatives_IB = ["IB", "ib", "Ib"]
		Alias_Alternatives_Charge = ["CHARGE", "Charge", "charge"]

		# Normalize IV Field
		for Alias in Alias_Alternatives_IV:

			# Check ID Field
			if Alias in values:
				
				# Set ID Field
				values["IV"] = values[Alias]

				# Break
				break

		# Normalize AC Field
		for Alias in Alias_Alternatives_AC:

			# Check Hardware Field
			if Alias in values:
				
				# Set Hardware Field
				values["AC"] = values[Alias]

				# Break
				break
		
		# Normalize SOC Field
		for Alias in Alias_Alternatives_SOC:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["SOC"] = values[Alias]

				# Break
				break

		# Normalize T Field
		for Alias in Alias_Alternatives_T:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["T"] = values[Alias]

				# Break
				break

		# Normalize FB Field
		for Alias in Alias_Alternatives_FB:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["FB"] = values[Alias]

				# Break
				break

		# Normalize IB Field
		for Alias in Alias_Alternatives_IB:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["IB"] = values[Alias]

				# Break
				break

		# Normalize Charge Field
		for Alias in Alias_Alternatives_Charge:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["Charge"] = values[Alias]

				# Break
				break

		# Return values
		return values

	# Value Validator
	@field_validator("IV", "AC", "SOC", "T", "FB", "IB")
	@classmethod
	def Validate_Values(cls, value):

		# Get Min and Max Values
		Min_Value = value.field_info.extra.get("min")
		Max_Value = value.field_info.extra.get("max")

		# Check Min Value
		if Min_Value is not None and value < Min_Value:
            
			# Set Value
			return -9999

		# Check Max Value
		if Max_Value is not None and value > Max_Value:
        
			# Set Value
			return 9999

		# Return Value
		return value

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
		Alias_Alternatives_Battery = ["BATTERY", "Battery", "battery", "BAT", "Bat", "bat"]

		# Normalize IV Field
		for Alias in Alias_Alternatives_Battery:

			# Check ID Field
			if Alias in values:
				
				# Set ID Field
				values["Battery"] = values[Alias]

				# Break
				break

		# Return values
		return values

# Define IoT Module
class Pack_IoT_Module(BaseModel):
	
	# GSM Module Firmware
	Firmware: Optional[str] = Field(default="", description="GSM modem firmware version.", example="13.00.007")

	# Module IMEI Number
	IMEI: Optional[str] = Field(default="", description="GSM modem IMEI number.", example="356156060000000", min_length=10, max_length=15)

	# Module Manufacturer
	Manufacturer: Optional[int] = Field(default=0, description="GSM modem manufacturer ID.", example=1, min=0, max=100)

	# Module Model
	Model: Optional[int] = Field(default=0, description="GSM modem model ID.", example=1, min=0, max=100)

	# Module Serial Number
	Serial: Optional[int] = Field(default=0, description="GSM modem serial ID.", example=20273, min=0)

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:
		
		# Set Alias Alternatives
		Alias_Alternatives_Firmware = ["FIRMWARE", "Firmware", "firmware", "FW", "fw", "Fw"]
		Alias_Alternatives_IMEI = ["IMEI", "Imei", "imei"]
		Alias_Alternatives_Manufacturer = ["MANUFACTURER", "Manufacturer", "Man", "man", "MF"]
		Alias_Alternatives_Model = ["MODEL", "Model", "model", "MD"]
		Alias_Alternatives_Serial = ["SERIAL", "Serial", "serial", "SR"]

		# Normalize Firmware Field
		for Alias in Alias_Alternatives_Firmware:

			# Check ID Field
			if Alias in values:
				
				# Set ID Field
				values["Firmware"] = values[Alias]

				# Break
				break

		# Normalize IMEI Field
		for Alias in Alias_Alternatives_IMEI:

			# Check Hardware Field
			if Alias in values:
				
				# Set Hardware Field
				values["IMEI"] = values[Alias]

				# Break
				break

		# Normalize Manufacturer Field
		for Alias in Alias_Alternatives_Manufacturer:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["Manufacturer"] = values[Alias]

				# Break
				break

		# Normalize Model Field
		for Alias in Alias_Alternatives_Model:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["Model"] = values[Alias]

				# Break
				break

		# Normalize Serial Field
		for Alias in Alias_Alternatives_Serial:

			# Check Firmware Field
			if Alias in values:
				
				# Set Firmware Field
				values["Serial"] = values[Alias]

				# Break
				break

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
	SIM_Type: Optional[int] = Field(default=0, description="SIM card type.", example=1, min=0, max=10)

	# SIM ICCID
	ICCID: str = Field(default="0000000000000000000", description="SIM card ICCID number.", example="8990011916180280000", min_length=10, max_length=20)

	# Operator Country Code
	MCC: Optional[int] = Field(default=0, description="Operator country code.", example=286, min=0, max=1000)

	# Operator Code
	MNC: Optional[int] = Field(default=0, description="Operator code.", example=1, min=0, max=1000)

	# RSSI
	RSSI: Optional[int] = Field(default=0, description="IoT RSSI signal level.", example=28, min=-100, max=100)

	# TAC
	TAC: Optional[str] = Field(default="0000", description="Operator type allocation code.", example="855E", min_length=3, max_length=5)

	# LAC
	LAC: Optional[str] = Field(default="0000", description="Operator base station location.", example="855E", min_length=3, max_length=5)

	# Cell ID
	Cell_ID: Optional[str] = Field(default="0000", description="Operator base station cell id.", example="E678", min_length=3, max_length=5)

	# IP
	IP: Optional[str] = Field(default="0.0.0.0", description="IoT IP address.", example="127.0.0.1", min_length=7, max_length=15)

	# Connection Time
	ConnTime: Optional[int] = Field(default=0, description="IoT connection time.", example=12, min=0, max=100000)

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:
		
		# Set Alias Alternatives
		Alias_Alternatives_SIM_Type = ["SIM_TYPE", "Sim_Type", "sim_type", "SIMTYPE", "SimType", "simtype", "SIM", "Sim", "sim"]
		Alias_Alternatives_ICCID = ["ICCID", "Iccid", "iccid"]
		Alias_Alternatives_MCC = ["MCC", "Mcc", "mcc"]
		Alias_Alternatives_MNC = ["MNC", "Mnc", "mnc"]
		Alias_Alternatives_RSSI = ["RSSI", "Rssi", "rssi", "DBM", "dBm", "dbm"]
		Alias_Alternatives_TAC = ["TAC", "Tac", "tac"]
		Alias_Alternatives_LAC = ["LAC", "Lac", "lac"]
		Alias_Alternatives_Cell_ID = ["CELL_ID", "Cell_Id", "cell_id", "CELLID", "CellId", "cellid"]
		Alias_Alternatives_IP = ["IP", "Ip", "ip"]
		Alias_Alternatives_ConnTime = ["CONNTIME", "ConnTime", "conntime", "CONNECTION_TIME", "Connection_Time", "connection_time", "CONNECTIONTIME", "ConnectionTime", "connectiontime"]

		# Normalize Sim Type Field
		for Alias in Alias_Alternatives_SIM_Type:

			# Check ID Field
			if Alias in values:

				# Set ID Field
				values["SIM_Type"] = values[Alias]

				# Break
				break

		# Normalize ICCID Field
		for Alias in Alias_Alternatives_ICCID:

			# Check Hardware Field
			if Alias in values:

				# Set Hardware Field
				values["ICCID"] = values[Alias]

				# Break
				break

		# Normalize MCC Field
		for Alias in Alias_Alternatives_MCC:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["MCC"] = values[Alias]

				# Break
				break

		# Normalize MNC Field
		for Alias in Alias_Alternatives_MNC:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["MNC"] = values[Alias]

				# Break
				break

		# Normalize RSSI Field
		for Alias in Alias_Alternatives_RSSI:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["RSSI"] = values[Alias]

				# Break
				break
		
		# Normalize TAC Field
		for Alias in Alias_Alternatives_TAC:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["TAC"] = values[Alias]

				# Break
				break
		
		# Normalize LAC Field
		for Alias in Alias_Alternatives_LAC:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["LAC"] = values[Alias]

				# Break
				break
		
		# Normalize Cell ID Field
		for Alias in Alias_Alternatives_Cell_ID:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["Cell_ID"] = values[Alias]

				# Break
				break

		# Normalize IP Field
		for Alias in Alias_Alternatives_IP:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["IP"] = values[Alias]

				# Break
				break
		
		# Normalize ConnTime Field
		for Alias in Alias_Alternatives_ConnTime:

			# Check Firmware Field
			if Alias in values:

				# Set Firmware Field
				values["ConnTime"] = values[Alias]

				# Break
				break

		# Return values
		return values

	# Value Validator
	@field_validator("SIM_Type", "MCC", "MNC", "RSSI", "ConnTime")
	@classmethod
	def Validate_Values(cls, value):

		# Get Min and Max Values
		Min_Value = value.field_info.extra.get("min")
		Max_Value = value.field_info.extra.get("max")
		
		# Check Min Value
		if Min_Value is not None and value < Min_Value:

			# Set Value
			return -9999

		# Check Max Value
		if Max_Value is not None and value > Max_Value:

			# Set Value
			return 9999

		# Return Value
		return value

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
		Alias_Alternatives_Module = ["MODULE", "Module", "module", "MD", "md", "Md"]
		Alias_Alternatives_Operator = ["OPERATOR", "Operator", "operator", "OP", "op", "Op"]

		# Normalize Module Field
		for Alias in Alias_Alternatives_Module:

			# Check ID Field
			if Alias in values:

				# Set ID Field
				values["Module"] = values[Alias]

				# Break
				break

		# Normalize Operator Field
		for Alias in Alias_Alternatives_Operator:

			# Check Hardware Field
			if Alias in values:

				# Set Hardware Field
				values["Operator"] = values[Alias]

				# Break
				break

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
		Alias_Alternatives_GSM = ["GSM", "Gsm", "gsm"]

		# Normalize GSM Field
		for Alias in Alias_Alternatives_GSM:

			# Check ID Field
			if Alias in values:

				# Set ID Field
				values["GSM"] = values[Alias]

				# Break
				break

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
		Alias_Alternatives_Info = ["INFO", "Info", "info"]
		Alias_Alternatives_Power = ["POWER", "Power", "power", "POW", "Pow", "pow"]
		Alias_Alternatives_IoT = ["IOT", "Iot", "iot"]

		# Normalize Info Field
		for Alias in Alias_Alternatives_Info:

			# Check Field
			if Alias in values:

				# Set Field
				values["Info"] = values[Alias]

				# Break
				break

		# Normalize Power Field
		for Alias in Alias_Alternatives_Power:

			# Check Field
			if Alias in values:

				# Set Field
				values["Power"] = values[Alias]

				# Break
				break
		
		# Normalize IoT Field
		for Alias in Alias_Alternatives_IoT:

			# Check Field
			if Alias in values:

				# Set Field
				values["IoT"] = values[Alias]

				# Break
				break

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
		Alias_Alternatives_Latitude = ["LATITUDE", "Latitude", "latitude", "LAT", "Lat", "lat"]
		Alias_Alternatives_Longtitude = ["LONGTITUDE", "Longtitude", "longtitude", "LONG", "Long", "long", "Longitude", "longitude", "LONGITUDE"]

		# Normalize Latitude Field
		for Alias in Alias_Alternatives_Latitude:

			# Check Field
			if Alias in values:

				# Set Field
				values["Latitude"] = values[Alias]

				# Break
				break

		# Normalize Longtitude Field
		for Alias in Alias_Alternatives_Longtitude:

			# Check Field
			if Alias in values:

				# Set Field
				values["Longtitude"] = values[Alias]

				# Break
				break

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
		Alias_Alternatives_AT = ["AT", "at", "At"]
		Alias_Alternatives_AH = ["AH", "ah", "Ah"]
		Alias_Alternatives_AP = ["AP", "ap", "Ap"]
		Alias_Alternatives_VL = ["VL", "vl", "Vl"]
		Alias_Alternatives_IL = ["IL", "il", "Il"]
		Alias_Alternatives_UV = ["UV", "uv", "Uv"]
		Alias_Alternatives_ST = ["ST", "st", "St"]
		Alias_Alternatives_R = ["R", "r", "Rain", "rain", "RAIN"]
		Alias_Alternatives_WD = ["WD", "wd", "Wd", "Wind", "wind", "WIND"]
		Alias_Alternatives_WS = ["WS", "ws", "Ws", "WindSpeed", "windspeed", "WINDSPEED"]

		# Normalize AT Field
		for Alias in Alias_Alternatives_AT:

			# Check Field
			if Alias in values:

				# Set Field
				values["AT"] = values[Alias]

				# Break
				break

		# Normalize AH Field
		for Alias in Alias_Alternatives_AH:

			# Check Field
			if Alias in values:

				# Set Field
				values["AH"] = values[Alias]

				# Break
				break

		# Normalize AP Field
		for Alias in Alias_Alternatives_AP:

			# Check Field
			if Alias in values:

				# Set Field
				values["AP"] = values[Alias]

				# Break
				break

		# Normalize VL Field
		for Alias in Alias_Alternatives_VL:

			# Check Field
			if Alias in values:

				# Set Field
				values["VL"] = values[Alias]

				# Break
				break
		
		# Normalize IR Field
		for Alias in Alias_Alternatives_IL:

			# Check Field
			if Alias in values:

				# Set Field
				values["IL"] = values[Alias]

				# Break
				break

		# Normalize UV Field
		for Alias in Alias_Alternatives_UV:

			# Check Field
			if Alias in values:

				# Set Field
				values["UV"] = values[Alias]

				# Break
				break

		# Normalize ST Field
		for Alias in Alias_Alternatives_ST:

			# Check Field
			if Alias in values:

				# Set Field
				values["ST"] = values[Alias]

				# Break
				break

		# Normalize R Field
		for Alias in Alias_Alternatives_R:

			# Check Field
			if Alias in values:

				# Set Field
				values["R"] = values[Alias]

				# Break
				break

		# Normalize WD Field
		for Alias in Alias_Alternatives_WD:

			# Check Field
			if Alias in values:

				# Set Field
				values["WD"] = values[Alias]

				# Break
				break

		# Normalize WS Field
		for Alias in Alias_Alternatives_WS:

			# Check Field
			if Alias in values:

				# Set Field
				values["WS"] = values[Alias]

				# Break
				break

		# Return values
		return values

	# Value Validator
	@field_validator("AT", "AH", "AP", "VL", "IL", "UV", "R", "WD", "WS")
	@classmethod
	def Validate_Values(cls, value):

		# Check Value
		if value is None:
			return None

		# Get Min and Max Values
		Min_Value = value.field_info.extra.get("min")
		Max_Value = value.field_info.extra.get("max")

		# Check Min Value
		if Min_Value is not None and value < Min_Value:
            
			# Set Value
			return -9999

		# Check Max Value
		if Max_Value is not None and value > Max_Value:
        
			# Set Value
			return 9999

		# Return Value
		return value

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
		Alias_Alternatives_Location = ["LOCATION", "Location", "location", "LOC", "Loc", "loc"]
		Alias_Alternatives_Environment = ["ENVIRONMENT", "Environment", "environment", "ENV", "Env", "env"]

		# Normalize Location Field
		for Alias in Alias_Alternatives_Location:

			# Check Field
			if Alias in values:

				# Set Field
				values["Location"] = values[Alias]

				# Break
				break

		# Normalize Environment Field
		for Alias in Alias_Alternatives_Environment:

			# Check Field
			if Alias in values:

				# Set Field
				values["Environment"] = values[Alias]

				# Break
				break

		# Return values
		return values

# Define payload
class Payload(BaseModel):

	# TimeStamp
	TimeStamp: str = Field(default="2022-07-19T08:28:32Z", description="Measurement time stamp.", example="2022-07-19T08:28:32Z")

	# WeatherStat Payload
	WeatherStat: Optional[Payload_WeatherStat]

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Alias_Alternatives_TimeStamp = ["TIMESTAMP", "TimeStamp", "timestamp", "TIME", "Time", "time", "TS", "Ts", "ts"]
		Alias_Alternatives_WeatherStat = ["WEATHERSTAT", "WeatherStat", "weatherstat", "WEATHER", "Weather", "weather", "WS", "Ws", "ws"]

		# Normalize TimeStamp Field
		for Alias in Alias_Alternatives_TimeStamp:

			# Check Field
			if Alias in values:

				# Set Field
				values["TimeStamp"] = values[Alias]

				# Break
				break

		# Normalize WeatherStat Field
		for Alias in Alias_Alternatives_WeatherStat:

			# Check Field
			if Alias in values:

				# Set Field
				values["WeatherStat"] = values[Alias]

				# Break
				break

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
	Command: str = Field(default="", description="Pack command.", example="Demo:PowerStat.Online")

	# Device
	Device: Optional[Pack_Device]

	# Payload
	Payload: Payload

	# Handle Field Names
	@root_validator(pre=True)
	def Normalize_Fields(cls, values: Dict) -> Dict:

		# Set Alias Alternatives
		Alias_Alternatives_Command = ["COMMAND", "Command", "command", "CMD", "Cmd", "cmd"]
		Alias_Alternatives_Device = ["DEVICE", "Device", "device", "DEV", "Dev", "dev"]
		Alias_Alternatives_Payload = ["PAYLOAD", "Payload", "payload", "PAY", "Pay", "pay"]

		# Normalize Command Field
		for Alias in Alias_Alternatives_Command:

			# Check Field
			if Alias in values:

				# Set Field
				values["Command"] = values[Alias]

				# Break
				break
		
		# Normalize Device Field
		for Alias in Alias_Alternatives_Device:

			# Check Field
			if Alias in values:

				# Set Field
				values["Device"] = values[Alias]

				# Break
				break

		# Normalize Payload Field
		for Alias in Alias_Alternatives_Payload:

			# Check Field
			if Alias in values:

				# Set Field
				values["Payload"] = values[Alias]

				# Break
				break

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
