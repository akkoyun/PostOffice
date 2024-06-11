# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re
from enum import IntEnum

# Define Constants
class Constants:

	# Info Constants
	class INFO:

		# Command Constants
		COMMAND_MIN_LENGTH = 3
		COMMAND_MAX_LENGTH = 10
		DEFAULT_COMMAND = "Unknown"
		COMMAND_ALLOWED = ["Online", "Offline", "Timed", "Interrupt", "Alarm"]

		# ID Constants
		ID_PATTERN = r'^[0-9A-F]{10,16}$'
		DEFAULT_ID = "0000000000000000"

		# Firmware Constants
		FIRMWARE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'
		DEFAULT_FIRMWARE = "00.00.00"

	# Define Battery Constants
	class BATTERY:

		# Define Battery Charge State
		class CHARGE_STATE(IntEnum):
			DISCHARGE = 0
			PRE_CHARGE = 1
			FAST_CHARGE = 2
			CHARGE_DONE = 3
			UNKNOWN = 9

		# Battery Voltage Constants
		VOLTAGE_MIN = 0.0
		VOLTAGE_MAX = 6.0
		DEFAULT_VOLTAGE = 0.0

		# Battery Current Constants
		CURRENT_MIN = -5000.0
		CURRENT_MAX = 5000.0
		DEFAULT_CURRENT = 0.0

		# Full Battery Capacity Constants
		CAPACITY_MIN = 0
		CAPACITY_MAX = 10000
		DEFAULT_CAPACITY = 0

		# Instant Battery Capacity Constants
		INSTANT_CAPACITY_MIN = 0
		INSTANT_CAPACITY_MAX = 10000
		DEFAULT_INSTANT_CAPACITY = 0

		# Battery State of Charge Constants
		SOC_MIN = 0.0
		SOC_MAX = 100.0
		DEFAULT_SOC = 0.0

		# Battery Temperature Constants
		TEMPERATURE_MIN = -50.0
		TEMPERATURE_MAX = 100.0
		DEFAULT_TEMPERATURE = 0.0

	# Define IoT Constants
	class IOT:

		# Define WDS Constants
		class WDS(IntEnum):
			CONNECTION_UNKNOWN = 0
			CONNECTION_2G = 1
			CONNECTION_3G = 2
			CONNECTION_4G = 3
			CONNECTION_TDSCDMA = 4

		# Firmware Version Constants
		FIRMWARE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{3}$'
		DEFAULT_FIRMWARE = "00.00.000"

		# IMEI Number Constants
		IMEI_PATTERN = r'^[0-9]{10,15}$'
		DEFAULT_IMEI = "000000000000000"
		IMEI_MIN_LENGTH = 10
		IMEI_MAX_LENGTH = 15

		# ICCID Number Constants
		ICCID_MIN_LENGTH = 10
		ICCID_MAX_LENGTH = 20
		ICCID_PATTERN = r'^[0-9]{10,20}$'
		DEFAULT_ICCID = "00000000000000000000"

		# RSSI Signal Level Constants
		RSSI_MIN = -100
		RSSI_MAX = 0
		DEFAULT_RSSI = 0

		# Connection Time Constants
		CONNECTION_TIME_MIN = 0
		CONNECTION_TIME_MAX = 100000
		DEFAULT_CONNECTION_TIME = 0

		# TAC Constants
		TAC_MIN = 0
		TAC_MAX = 65535
		DEFAULT_TAC = 0

		# LAC Constants
		LAC_MIN = 0
		LAC_MAX = 65535
		DEFAULT_LAC = 0

		# Cell ID Constants
		CELL_ID_MIN = 0
		CELL_ID_MAX = 65535
		DEFAULT_CELL_ID = 0

# Define IoT Data Base Model

# Custom Base Model
class CustomBaseModel(BaseModel):
    def model_dump(self, **kwargs):
        kwargs['exclude_none'] = True
        return super().model_dump(**kwargs)

# Define Info
class Info(CustomBaseModel):

	# Define Command
	Command: str = Field(description="Pack command.", example="Online", min_length=Constants.INFO.COMMAND_MIN_LENGTH, max_length=Constants.INFO.COMMAND_MAX_LENGTH, default=Constants.INFO.DEFAULT_COMMAND)

	# Command Validator
	@field_validator("Command", mode='before')
	def Command_Validator(cls, command):
		
		# Return Command
		return command if command in Constants.INFO.COMMAND_ALLOWED else Constants.INFO.DEFAULT_COMMAND

	# Timestamp
	TimeStamp: str = Field(..., description="Measurement time stamp.", example="2022-07-19T08:28:32")

	# Timestamp Validator
	@field_validator('TimeStamp', mode='before')
	def TimeStamp_Validator(cls, v):

		try:

			# Check for Z
			if 'Z' in v:
				v = v.replace('Z', '+00:00')

			# Check for +
			v = re.sub(r'\+\d{2}:\d{2}', '', v)

			# Parse Date
			Parsed_TimeStamp = datetime.fromisoformat(v)

			# Return Value
			return Parsed_TimeStamp.strftime('%Y-%m-%dT%H:%M:%S')
        
		except ValueError:

			# Set Default Value
			return "2024-01-01T00:00:00"

	# Device ID
	ID: str = Field(description="IoT device unique ID.", example="8B00000000000000", default=Constants.INFO.DEFAULT_ID)

	# Device ID Validator
	@field_validator('ID', mode='before')
	def ID_Validator(cls, id_value):

		# Check ID
		if not re.match(Constants.INFO.ID_PATTERN, id_value):
        
			# Set Default Value
			id_value = Constants.INFO.DEFAULT_ID

		# Return ID
		return id_value

	# Device Firmware Version
	Firmware: Optional[str] = Field(description="Firmware version of device.", example="01.00.00", default=Constants.INFO.DEFAULT_FIRMWARE)

	# Firmware Validator
	@field_validator('Firmware', mode='before')
	def Firmware_Validator(cls, value):

		# Check Value
		if not re.match(Constants.INFO.FIRMWARE_PATTERN, value):

			# Set Default Value
			value = Constants.INFO.DEFAULT_FIRMWARE

		# Return Value
		return value

# Define Power
class Power(CustomBaseModel):
	
	# Instant Battery Voltage
	B_IV: float = Field(description="Battery instant voltage.", example=3.8, ge=Constants.BATTERY.VOLTAGE_MIN, le=Constants.BATTERY.VOLTAGE_MAX, default=Constants.BATTERY.DEFAULT_VOLTAGE)

	# Battery Instant Voltage Validator
	@field_validator('B_IV', mode='before')
	def B_IV_Validator(cls, value):

		# Check Value
		if value is None or not Constants.BATTERY.VOLTAGE_MIN <= value <= Constants.BATTERY.VOLTAGE_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_VOLTAGE

		# Return Value
		return value

	# Average Battery Current
	B_AC: float = Field(description="Battery average current.", example=0.2, ge=Constants.BATTERY.CURRENT_MIN, le=Constants.BATTERY.CURRENT_MAX, default=Constants.BATTERY.DEFAULT_CURRENT)

	# Battery Average Current Validator
	@field_validator('B_AC', mode='before')
	def B_AC_Validator(cls, value):

		# Check Value
		if value is None or not Constants.BATTERY.CURRENT_MIN <= value <= Constants.BATTERY.CURRENT_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_CURRENT

		# Return Value
		return value

	# Full Battery Capacity
	B_FC: Optional[int] = Field(description="Full battery capacity.", example=2000, ge=Constants.BATTERY.CAPACITY_MIN, le=Constants.BATTERY.CAPACITY_MAX, default=Constants.BATTERY.DEFAULT_CAPACITY)

	# Full Battery Capacity Validator
	@field_validator('B_FC', mode='before')
	def B_FC_Validator(cls, value):

		# Check Value
		if value is not None and not Constants.BATTERY.CAPACITY_MIN <= value <= Constants.BATTERY.CAPACITY_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_CAPACITY

		# Return Value
		return value

	# Instant Battery Capacity
	B_IC: Optional[int] = Field(description="Instant battery capacity.", example=1820, ge=Constants.BATTERY.INSTANT_CAPACITY_MIN, le=Constants.BATTERY.INSTANT_CAPACITY_MAX, default=Constants.BATTERY.DEFAULT_INSTANT_CAPACITY)

	# Instant Battery Capacity Validator
	@field_validator('B_IC', mode='before')
	def B_IC_Validator(cls, value):

		# Check Value
		if value is not None and not Constants.BATTERY.INSTANT_CAPACITY_MIN <= value <= Constants.BATTERY.INSTANT_CAPACITY_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_INSTANT_CAPACITY

		# Return Value
		return value

	# Battery State of Charge
	B_SOC: float = Field(description="Battery state of charge.", example=97.30, ge=Constants.BATTERY.SOC_MIN, le=Constants.BATTERY.SOC_MAX, default=Constants.BATTERY.DEFAULT_SOC)

	# Battery State of Charge Validator
	@field_validator('B_SOC', mode='before')
	def B_SOC_Validator(cls, value):

		# Check Value
		if value is None or not Constants.BATTERY.SOC_MIN <= value <= Constants.BATTERY.SOC_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_SOC

		# Return Value
		return value

	# Battery Temperature
	B_T: Optional[float] = Field(description="Battery temperature.", example=32.1903, ge=Constants.BATTERY.TEMPERATURE_MIN, le=Constants.BATTERY.TEMPERATURE_MAX, default=Constants.BATTERY.DEFAULT_TEMPERATURE)

	# Battery Temperature Validator
	@field_validator('B_T', mode='before')
	def B_T_Validator(cls, value):

		# Check Value
		if value is not None and not Constants.BATTERY.TEMPERATURE_MIN <= value <= Constants.BATTERY.TEMPERATURE_MAX:

			# Set Default Value
			value = Constants.BATTERY.DEFAULT_TEMPERATURE

		# Return Value
		return value

	# Battery Charge State
	B_CS: int = Field(description="Battery charge state.", examples=Constants.BATTERY.CHARGE_STATE.UNKNOWN, default=Constants.BATTERY.CHARGE_STATE.UNKNOWN)

	# Battery Charge State Validator
	@field_validator('B_CS', mode='before')
	def Battery_Charge_State_Validator(cls, value):

		# Check Value
		if value is None or not isinstance(value, Constants.BATTERY.CHARGE_STATE):

			# Set Default Value
			value = Constants.BATTERY.CHARGE_STATE.UNKNOWN

		# Return Value
		return value

# Define IoT
class IoT(CustomBaseModel):

	# GSM Module Firmware
	Firmware: Optional[str] = Field(description="Modem firmware version.", example="13.00.007", default=Constants.IOT.DEFAULT_FIRMWARE)

	# Firmware Validator
	@field_validator('Firmware', mode='before')
	def Firmware_Validator(cls, value):

		# Check Value
		if not re.match(Constants.IOT.FIRMWARE_PATTERN, value) or None:

			# Set Default Value
			value = Constants.IOT.DEFAULT_FIRMWARE

		# Return Value
		return value

	# Module IMEI Number
	IMEI: Optional[str] = Field(description="GSM modem IMEI number.", example="356156060000000", min_length=Constants.IOT.IMEI_MIN_LENGTH, max_length=Constants.IOT.IMEI_MAX_LENGTH, default=Constants.IOT.DEFAULT_IMEI)

	# IMEI Validator
	@field_validator('IMEI', mode='before')
	def IMEI_Validator(cls, value):

		# Check Value
		if not re.match(Constants.IOT.IMEI_PATTERN, value) or None:

			# Set Default Value
			value = Constants.IOT.DEFAULT_IMEI

		# Return Value
		return value

	# SIM ICCID
	ICCID: str = Field(description="SIM card ICCID number.", example="8990011916180280000", min_length=Constants.IOT.ICCID_MIN_LENGTH, max_length=Constants.IOT.ICCID_MAX_LENGTH, default=Constants.IOT.DEFAULT_ICCID)

	# ICCID Validator
	@field_validator('ICCID', mode='before')
	def ICCID_Validator(cls, value):

		# Check Value
		if not re.match(Constants.IOT.ICCID_PATTERN, value) or None:

			# Set Default Value
			value = Constants.IOT.DEFAULT_ICCID

		# Return Value
		return value

	# RSSI
	RSSI: Optional[int] = Field(description="IoT RSSI signal level.", example=28, ge=Constants.IOT.RSSI_MIN, le=Constants.IOT.RSSI_MAX, default=Constants.IOT.DEFAULT_RSSI)

	# RSSI Validator
	@field_validator('RSSI', mode='before')
	def RSSI_Validator(cls, value):

		# Check Value
		if value is (value < Constants.IOT.RSSI_MIN or value > Constants.IOT.RSSI_MAX):

			# Set Default Value
			value = Constants.IOT.DEFAULT_RSSI

		# Return Value
		return value

	# Connection Time
	ConnTime: Optional[int] = Field(description="IoT connection time.", example=12, ge=Constants.IOT.CONNECTION_TIME_MIN, le=Constants.IOT.CONNECTION_TIME_MAX, default=Constants.IOT.DEFAULT_CONNECTION_TIME)

	# Connection Time Validator
	@field_validator('ConnTime', mode='before')
	def ConnTime_Validator(cls, value):

		# Check Value
		if value is (value < Constants.IOT.CONNECTION_TIME_MIN or value > Constants.IOT.CONNECTION_TIME_MAX):

			# Set Default Value
			value = Constants.IOT.DEFAULT_CONNECTION_TIME

		# Return Value
		return value

	# TAC
	TAC: Optional[int] = Field(description="Operator type allocation code.", example=34124, ge=Constants.IOT.TAC_MIN, le=Constants.IOT.TAC_MAX, default=Constants.IOT.DEFAULT_TAC)

	# TAC Validator
	@field_validator("TAC", mode='before')
	def TAC_Validator(cls, value):

		# Check Value
		if value is (value < Constants.IOT.TAC_MIN or value > Constants.IOT.TAC_MAX):

			# Set Default Value
			value = Constants.IOT.DEFAULT_TAC

		# Return Value
		return value

	# LAC
	LAC: Optional[int] = Field(description="Operator base station location.", example=34124, ge=Constants.IOT.LAC_MIN, le=Constants.IOT.LAC_MAX, default=Constants.IOT.DEFAULT_LAC)

	# LAC Validator
	@field_validator("LAC", mode='before')
	def LAC_Validator(cls, value):

		# Check Value
		if value is (value < Constants.IOT.LAC_MIN or value > Constants.IOT.LAC_MAX):

			# Set Default Value
			value = Constants.IOT.DEFAULT_LAC

		# Return Value
		return value

	# Cell ID
	Cell_ID: Optional[int] = Field(description="Operator base station cell id.", example=34124, ge=Constants.IOT.CELL_ID_MIN, le=Constants.IOT.CELL_ID_MAX, default=Constants.IOT.DEFAULT_CELL_ID)

	# Cell ID Validator
	@field_validator("Cell_ID", mode='before')
	def Cell_ID_Validator(cls, value):

		# Check Value
		if value is (value < Constants.IOT.CELL_ID_MIN or value > Constants.IOT.CELL_ID_MAX):

			# Set Default Value
			value = Constants.IOT.DEFAULT_CELL_ID

		# Return Value
		return value

	# WDS
	WDS: Optional[int] = Field(description="IoT WDS type.", example=Constants.IOT.WDS.CONNECTION_4G, default=Constants.IOT.WDS.CONNECTION_UNKNOWN)

	# WDS Validator
	@field_validator('WDS', mode='before')
	def WDS_Validator(cls, value):

		# Check Value
		if value is None or not isinstance(value, Constants.IOT.WDS):

			# Set Default Value
			value = Constants.IOT.WDS.CONNECTION_UNKNOWN

		# Return Value
		return value

# Define Device
class Device(CustomBaseModel):

	# Device Power
	Power: Power

	# Device IoT
	IoT: IoT

# Define Payload payload
class Payload(CustomBaseModel):

	# Last Measured PCB Temperature Value
	PCB_T: Optional[float] = Field(description="PCB temperature.", example=28.3232)

	# Last Measured PCB Humidity Value
	PCB_H: Optional[float] = Field(description="PCB humidity.", example=85.2332)

	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(description="Air temperature.", example=28.3232)
	AT2: Optional[float] = Field(description="Air temperature.", example=28.3232)
	AT3: Optional[float] = Field(description="Air temperature.", example=28.3232)
	AT4: Optional[float] = Field(description="Air temperature.", example=28.3232)
	AT5: Optional[float] = Field(description="Air temperature.", example=28.3232)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(description="Air humidity.", example=85.2332)
	AH2: Optional[float] = Field(description="Air humidity.", example=85.2332)
	AH3: Optional[float] = Field(description="Air humidity.", example=85.2332)
	AH4: Optional[float] = Field(description="Air humidity.", example=85.2332)
	AH5: Optional[float] = Field(description="Air humidity.", example=85.2332)

	# Last Measured Feels Like Temperature Value
	AT_FL: Optional[float] = Field(description="Feels like temperature.", example=28.3232)
	AT2_FL: Optional[float] = Field(description="Feels like temperature.", example=28.3232)
	AT3_FL: Optional[float] = Field(description="Feels like temperature.", example=28.3232)
	AT4_FL: Optional[float] = Field(description="Feels like temperature.", example=28.3232)
	AT5_FL: Optional[float] = Field(description="Feels like temperature.", example=28.3232)

	# Last Measured Dew Point Value
	AT_Dew: Optional[float] = Field(description="Dew point.", example=28.3232)
	AT2_Dew: Optional[float] = Field(description="Dew point.", example=28.3232)
	AT3_Dew: Optional[float] = Field(description="Dew point.", example=28.3232)
	AT4_Dew: Optional[float] = Field(description="Dew point.", example=28.3232)
	AT5_Dew: Optional[float] = Field(description="Dew point.", example=28.3232)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(description="Air pressure.", example=985.55)
	AP2: Optional[float] = Field(description="Air pressure.", example=985.55)
	AP3: Optional[float] = Field(description="Air pressure.", example=985.55)
	AP4: Optional[float] = Field(description="Air pressure.", example=985.55)
	AP5: Optional[float] = Field(description="Air pressure.", example=985.55)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(description="Visual light.", example=1234)
	VL2: Optional[int] = Field(description="Visual light.", example=1234)
	VL3: Optional[int] = Field(description="Visual light.", example=1234)
	VL4: Optional[int] = Field(description="Visual light.", example=1234)
	VL5: Optional[int] = Field(description="Visual light.", example=1234)

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(description="Infrared light.", example=1234)
	IR2: Optional[int] = Field(description="Infrared light.", example=1234)
	IR3: Optional[int] = Field(description="Infrared light.", example=1234)
	IR4: Optional[int] = Field(description="Infrared light.", example=1234)
	IR5: Optional[int] = Field(description="Infrared light.", example=1234)

	# Last Measured UV Value
	UV: Optional[float] = Field(description="UV index.", example=2.12)
	UV2: Optional[float] = Field(description="UV index.", example=2.12)
	UV3: Optional[float] = Field(description="UV index.", example=2.12)
	UV4: Optional[float] = Field(description="UV index.", example=2.12)
	UV5: Optional[float] = Field(description="UV index.", example=2.12)

	# Last Measured Soil Temperature Value (Array)
	ST: Optional[list[Optional[float]]] = Field(description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=0, max_items=10)

	# Last Measured Soil Temperature Value (Single)
	ST0: Optional[float] = Field(description="10 cm Soil temperature.", example=28.12)
	ST1: Optional[float] = Field(description="20 cm Soil temperature.", example=27.12)
	ST2: Optional[float] = Field(description="30 cm Soil temperature.", example=26.12)
	ST3: Optional[float] = Field(description="40 cm Soil temperature.", example=25.12)
	ST4: Optional[float] = Field(description="50 cm Soil temperature.", example=24.12)
	ST5: Optional[float] = Field(description="60 cm Soil temperature.", example=23.12)
	ST6: Optional[float] = Field(description="70 cm Soil temperature.", example=22.12)
	ST7: Optional[float] = Field(description="80 cm Soil temperature.", example=21.12)
	ST8: Optional[float] = Field(description="90 cm Soil temperature.", example=20.12)
	ST9: Optional[float] = Field(description="100 cm Soil temperature.", example=19.12)

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25)

	# GPS Data
	Latitude: Optional[float] = Field(description="GNSS lattitude value.", example=1.243242342)
	Longitude: Optional[float] = Field(description="GNSS longitude value.", example=23.3213232)
	Altitude: Optional[float] = Field(description="GNSS altitude value.", example=123.123)
	Speed: Optional[float] = Field(description="GNSS speed value.", example=123.123)
	Head: Optional[float] = Field(description="GNSS heading value.", example=123.123)
	H_Acc: Optional[float] = Field(description="GNSS horizontal accuracy value.", example=123.123)
	V_Acc: Optional[float] = Field(description="GNSS vertical accuracy value.", example=123.123)
	P_Acc: Optional[float] = Field(description="GNSS position accuracy value.", example=123.123)
	Fix: Optional[int] = Field(description="GNSS position fix type value.", example=123)

	# Instant Voltage Value
	V: Optional[list[Optional[float]]] = Field(description="Instant voltage measurement", example=[220.12, 222.12, 235.12, 225.12], min_items=0, max_items=4)
	V_R: Optional[float] = Field(description="Phase R instant voltage measurement", example=220.12)
	V_S: Optional[float] = Field(description="Phase S instant voltage measurement", example=220.12)
	V_T: Optional[float] = Field(description="Phase T instant voltage measurement", example=220.12)
	V_A: Optional[float] = Field(description="Instant voltage average measurement", example=220.12)

	# Min Instant Voltage Value
	V_MIN_R: Optional[float] = Field(description="Phase R minimum voltage measurement", example=220.12)
	V_MIN_S: Optional[float] = Field(description="Phase S minimum voltage measurement", example=220.12)
	V_MIN_T: Optional[float] = Field(description="Phase T minimum voltage measurement", example=220.12)

	# Max Instant Voltage Value
	V_MAX_R: Optional[float] = Field(description="Phase R maximum voltage measurement", example=220.12)
	V_MAX_S: Optional[float] = Field(description="Phase S maximum voltage measurement", example=220.12)
	V_MAX_T: Optional[float] = Field(description="Phase T maximum voltage measurement", example=220.12)

	# RMS Voltage Value
	VRMS: Optional[list[Optional[float]]] = Field(description="RMS voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VRMS_R: Optional[float] = Field(description="Phase R RMS voltage measurement", example=220.12)
	VRMS_S: Optional[float] = Field(description="Phase S RMS voltage measurement", example=220.12)
	VRMS_T: Optional[float] = Field(description="Phase T RMS voltage measurement", example=220.12)
	VRMS_A: Optional[float] = Field(description="RMS voltage average measurement", example=220.12)

	# Min RMS Voltage Value
	VRMS_MIN_R: Optional[float] = Field(description="Phase R minimum voltage measurement", example=220.12)
	VRMS_MIN_S: Optional[float] = Field(description="Phase S minimum voltage measurement", example=220.12)
	VRMS_MIN_T: Optional[float] = Field(description="Phase T minimum voltage measurement", example=220.12)

	# Max RMS Voltage Value
	VRMS_MAX_R: Optional[float] = Field(description="Phase R maximum voltage measurement", example=220.12)
	VRMS_MAX_S: Optional[float] = Field(description="Phase S maximum voltage measurement", example=220.12)
	VRMS_MAX_T: Optional[float] = Field(description="Phase T maximum voltage measurement", example=220.12)

	# Fundamental Voltage Value
	VFun: Optional[list[Optional[float]]] = Field(description="Fundamental voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VFun_R: Optional[float] = Field(description="Phase R fundamental voltage measurement", example=220.12)
	VFun_S: Optional[float] = Field(description="Phase S fundamental voltage measurement", example=220.12)
	VFun_T: Optional[float] = Field(description="Phase T fundamental voltage measurement", example=220.12)
	VFun_A: Optional[float] = Field(description="Fundamental voltage average measurement", example=220.12)

	# Harmonic Voltage Value
	VHarm: Optional[list[Optional[float]]] = Field(description="Harmonic voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VHarm_R: Optional[float] = Field(description="Phase R harmonic voltage measurement", example=220.12)
	VHarm_S: Optional[float] = Field(description="Phase S harmonic voltage measurement", example=220.12)
	VHarm_T: Optional[float] = Field(description="Phase T harmonic voltage measurement", example=220.12)
	VHarm_A: Optional[float] = Field(description="Harmonic voltage average measurement", example=220.12)

	# Frequency Value
	FQ: Optional[float] = Field(description="Frequency measurement", example=50.12)

	# Instant Current Value
	I: Optional[list[Optional[float]]] = Field(description="Instant current measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	I_R: Optional[float] = Field(description="Phase R instant current measurement", example=20.12)
	I_S: Optional[float] = Field(description="Phase S instant current measurement", example=20.12)
	I_T: Optional[float] = Field(description="Phase T instant current measurement", example=20.12)
	I_A: Optional[float] = Field(description="Instant current average measurement", example=20.12)

	# Peak Current Value
	IP: Optional[list[Optional[float]]] = Field(description="Peak current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IP_R: Optional[float] = Field(description="Phase R peak current measurement", example=20.12)
	IP_S: Optional[float] = Field(description="Phase S peak current measurement", example=20.12)
	IP_T: Optional[float] = Field(description="Phase T peak current measurement", example=20.12)
	IP_A: Optional[float] = Field(description="Peak current average measurement", example=20.12)

	# RMS Current Value
	IRMS: Optional[list[Optional[float]]] = Field(description="RMS current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IRMS_R: Optional[float] = Field(description="Phase R RMS current measurement", example=20.12)
	IRMS_S: Optional[float] = Field(description="Phase S RMS current measurement", example=20.12)
	IRMS_T: Optional[float] = Field(description="Phase T RMS current measurement", example=20.12)
	IRMS_A: Optional[float] = Field(description="RMS current average measurement", example=20.12)

	# Fundamental Current Value
	IFun: Optional[list[Optional[float]]] = Field(description="Fundamental current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IFun_R: Optional[float] = Field(description="Phase R fundamental current measurement", example=20.12)
	IFun_S: Optional[float] = Field(description="Phase S fundamental current measurement", example=20.12)
	IFun_T: Optional[float] = Field(description="Phase T fundamental current measurement", example=20.12)
	IFun_A: Optional[float] = Field(description="Fundamental current average measurement", example=20.12)

	# Harmonic Current Value
	IHarm: Optional[list[Optional[float]]] = Field(description="Harmonic current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IHarm_R: Optional[float] = Field(description="Phase R harmonic current measurement", example=20.12)
	IHarm_S: Optional[float] = Field(description="Phase S harmonic current measurement", example=20.12)
	IHarm_T: Optional[float] = Field(description="Phase T harmonic current measurement", example=20.12)
	IHarm_A: Optional[float] = Field(description="Harmonic current average measurement", example=20.12)

	# Active Power Value
	P: Optional[list[Optional[float]]] = Field(description="Active power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	P_R: Optional[float] = Field(description="Phase R active power measurement", example=220.12)
	P_S: Optional[float] = Field(description="Phase S active power measurement", example=220.12)
	P_T: Optional[float] = Field(description="Phase T active power measurement", example=220.12)
	P_A: Optional[float] = Field(description="Active power average measurement", example=220.12)

	# Reactive Power Value
	Q: Optional[list[Optional[float]]] = Field(description="Reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	Q_R: Optional[float] = Field(description="Phase R reactive power measurement", example=220.12)
	Q_S: Optional[float] = Field(description="Phase S reactive power measurement", example=220.12)
	Q_T: Optional[float] = Field(description="Phase T reactive power measurement", example=220.12)
	Q_A: Optional[float] = Field(description="Reactive power average measurement", example=220.12)

	# Apparent Power Value
	S: Optional[list[Optional[float]]] = Field(description="Apparent power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	S_R: Optional[float] = Field(description="Phase R apparent power measurement", example=220.12)
	S_S: Optional[float] = Field(description="Phase S apparent power measurement", example=220.12)
	S_T: Optional[float] = Field(description="Phase T apparent power measurement", example=220.12)
	S_A: Optional[float] = Field(description="Apparent power average measurement", example=220.12)

	# Fundamental Reactive Power Value
	QFun: Optional[list[Optional[float]]] = Field(description="Fundamental reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	QFun_R: Optional[float] = Field(description="Phase R fundamental reactive power measurement", example=220.12)
	QFun_S: Optional[float] = Field(description="Phase S fundamental reactive power measurement", example=220.12)
	QFun_T: Optional[float] = Field(description="Phase T fundamental reactive power measurement", example=220.12)
	QFun_A: Optional[float] = Field(description="Fundamental reactive power average measurement", example=220.12)

	# Harmonic Reactive Power Value
	QHarm: Optional[list[Optional[float]]] = Field(description="Harmonic reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	QHarm_R: Optional[float] = Field(description="Phase R harmonic reactive power measurement", example=220.12)
	QHarm_S: Optional[float] = Field(description="Phase S harmonic reactive power measurement", example=220.12)
	QHarm_T: Optional[float] = Field(description="Phase T harmonic reactive power measurement", example=220.12)
	QHarm_A: Optional[float] = Field(description="Harmonic reactive power average measurement", example=220.12)

	# Fundamental Power Value
	PFun: Optional[list[Optional[float]]] = Field(description="Fundamental power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	PFun_R: Optional[float] = Field(description="Phase R fundamental power measurement", example=220.12)
	PFun_S: Optional[float] = Field(description="Phase S fundamental power measurement", example=220.12)
	PFun_T: Optional[float] = Field(description="Phase T fundamental power measurement", example=220.12)
	PFun_A: Optional[float] = Field(description="Fundamental power average measurement", example=220.12)

	# Harmonic Power Value
	PHarm: Optional[list[Optional[float]]] = Field(description="Harmonic power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	PHarm_R: Optional[float] = Field(description="Phase R harmonic power measurement", example=220.12)
	PHarm_S: Optional[float] = Field(description="Phase S harmonic power measurement", example=220.12)
	PHarm_T: Optional[float] = Field(description="Phase T harmonic power measurement", example=220.12)
	PHarm_A: Optional[float] = Field(description="Harmonic power average measurement", example=220.12)

	# Fundamental Volt Amper 
	FunVA: Optional[list[Optional[float]]] = Field(description="Fundamental volt ampere measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	FunVA_R: Optional[float] = Field(description="Phase R fundamental volt ampere measurement", example=220.12)
	FunVA_S: Optional[float] = Field(description="Phase S fundamental volt ampere measurement", example=220.12)
	FunVA_T: Optional[float] = Field(description="Phase T fundamental volt ampere measurement", example=220.12)
	FunVA_A: Optional[float] = Field(description="Fundamental volt ampere average measurement", example=220.12)

	# Power Factor Value
	PF: Optional[list[Optional[float]]] = Field(description="Power factor measurement", example=[0.812, 0.812, 0.812, 0.812], min_items=0, max_items=4)
	PF_R: Optional[float] = Field(description="Phase R power factor measurement", example=0.81)
	PF_S: Optional[float] = Field(description="Phase S power factor measurement", example=0.81)
	PF_T: Optional[float] = Field(description="Phase T power factor measurement", example=0.81)
	PF_A: Optional[float] = Field(description="Power factor average measurement", example=0.81)

	# Active Energy Value
	AE: Optional[list[Optional[float]]] = Field(description="Active energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	AE_R: Optional[float] = Field(description="Phase R active energy measurement", example=220.12)
	AE_S: Optional[float] = Field(description="Phase S active energy measurement", example=220.12)
	AE_T: Optional[float] = Field(description="Phase T active energy measurement", example=220.12)
	AE_A: Optional[float] = Field(description="Active energy average measurement", example=220.12)
	AE_TOT: Optional[float] = Field(description="Active energy total measurement", example=220.12)

	# Reactive Energy Leading Value
	RE_L: Optional[list[Optional[float]]] = Field(description="Reactive leading energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	RE_L_R: Optional[float] = Field(description="Phase R leading reactive energy measurement", example=220.12)
	RE_L_S: Optional[float] = Field(description="Phase S leading reactive energy measurement", example=220.12)
	RE_L_T: Optional[float] = Field(description="Phase T leading reactive energy measurement", example=220.12)
	RE_L_A: Optional[float] = Field(description="Reactive leading energy average measurement", example=220.12)
	RE_L_TOT: Optional[float] = Field(description="Total leading reactive energy measurement", example=220.12)

	# Reactive Energy Lagging Value
	RE_G: Optional[list[Optional[float]]] = Field(description="Reactive lagging energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	RE_G_R: Optional[float] = Field(description="Phase R lagging reactive energy measurement", example=220.12)
	RE_G_S: Optional[float] = Field(description="Phase S lagging reactive energy measurement", example=220.12)
	RE_G_T: Optional[float] = Field(description="Phase T lagging reactive energy measurement", example=220.12)
	RE_G_A: Optional[float] = Field(description="Reactive lagging energy average measurement", example=220.12)
	RE_G_TOT: Optional[float] = Field(description="Total lagging reactive energy measurement", example=220.12)

	# Register Values
	STATUS: Optional[int] = Field(description="Device status register value.", example=0)
	STOP: Optional[int] = Field(description="Device stop register value.", example=0)

	# Pump Run Time Value
	T_Pump: Optional[float] = Field(description="Pump run time measurement", example=20.12)

	# Energy Min Max Values
	IRMS_MAX_R: Optional[float] = Field(description="Phase R maximum current measurement", example=20.12)
	IRMS_MAX_S: Optional[float] = Field(description="Phase S maximum current measurement", example=20.12)
	IRMS_MAX_T: Optional[float] = Field(description="Phase T maximum current measurement", example=20.12)
	FQ_MIN: Optional[float] = Field(description="Minimum frequency measurement", example=50.12)
	FQ_MAX: Optional[float] = Field(description="Maximum frequency measurement", example=50.12)
	PF_MIN_R: Optional[float] = Field(description="Phase R minimum active power measurement", example=0.8)
	PF_MAX_R: Optional[float] = Field(description="Phase R maximum active power measurement", example=0.8)
	PF_MIN_S: Optional[float] = Field(description="Phase S minimum active power measurement", example=0.8)
	PF_MAX_S: Optional[float] = Field(description="Phase S maximum active power measurement", example=0.8)
	PF_MIN_T: Optional[float] = Field(description="Phase T minimum active power measurement", example=0.8)
	PF_MAX_T: Optional[float] = Field(description="Phase T maximum active power measurement", example=0.8)

	# Energy Set Values
	V_Set_Min: Optional[float] = Field(description="Minimum voltage set value.", example=220.12)
	V_Set_Max: Optional[float] = Field(description="Maximum voltage set value.", example=220.12)

	# FOTA Parameters
	Firmware_ID: Optional[float] = Field(description="Firmware ID.", example=2)
	FOTA_Download_Status: Optional[float] = Field(description="FOTA download status.", example=2)
	FOTA_Download_Time: Optional[float] = Field(description="FOTA download time.", example=2)

# Define IoT RAW Data Base Model
class Data_Pack(CustomBaseModel):

	# Info
	Info: Info

	# Device
	Device: Device

	# Payload
	Payload: Payload
