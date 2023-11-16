# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
from datetime import datetime
from dateutil import parser
import re
from Setup.Config import Payload_Limits as Limits

# Define IoT Data Base Model
# Version 01.00.00

# Custom Base Model
class CustomBaseModel(BaseModel):
    def dict(self, **kwargs):
        kwargs['exclude_none'] = True
        return super().dict(**kwargs)

# Define Info
class Info(CustomBaseModel):

	# Define Command
	Command: str = Field(description="Pack command.", example="Online")
    
	# Timestamp
	TimeStamp: str = Field(description="Measurement time stamp.", example="2022-07-19 08:28:32")
	
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

	# Timestamp Validator
	@validator('TimeStamp')
	def validate_timestamp(cls, v):

		# Check Timestamp
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
		
		# Raise Error
		except ValueError:
			
			# Raise Error
			raise ValueError('TimeStamp is not in a valid format')

# Define Power
class Power(CustomBaseModel):
	
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
class IoT(CustomBaseModel):

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

# Define Device
class Device(CustomBaseModel):
    
	# Device Power
	Power: Power

	# Device IoT
	IoT: IoT

# Define Payload payload
class Payload(CustomBaseModel):

	# Latitude Value of Device
	Latitude: Optional[float] = Field(description="GNSS lattitude value.", example=1.243242342, min=Limits.LATITUDE_MIN, max=Limits.LATITUDE_MAX)

	# Longitude Value of Device
	Longitude: Optional[float] = Field(description="GNSS longitude value.", example=23.3213232, min=Limits.LONGITUDE_MIN, max=Limits.LONGITUDE_MAX)

	# Last Measured PCB Temperature Value
	PCB_T: Optional[float] = Field(description="PCB temperature.", example=28.3232, min=Limits.PCB_TEMPERATURE_MIN, max=Limits.PCB_TEMPERATURE_MAX)

	# Last Measured PCB Humidity Value
	PCB_H: Optional[float] = Field(description="PCB humidity.", example=85.2332, min=Limits.PCB_HUMIDITY_MIN, max=Limits.PCB_HUMIDITY_MAX)

	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(description="Air temperature.", example=28.3232, min=Limits.AT_MIN, max=Limits.AT_MAX)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(description="Air humidity.", example=85.2332, min=Limits.AH_MIN, max=Limits.AH_MAX)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(description="Air pressure.", example=985.55, min=Limits.AP_MIN, max=Limits.AP_MAX)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(description="Visual light.", example=1234, min=Limits.VL_MIN, max=Limits.VL_MAX)

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(description="Infrared light.", example=1234, min=Limits.IR_MIN, max=Limits.IR_MAX)

	# Last Measured UV Value
	UV: Optional[float] = Field(description="UV index.", example=2.12, min=Limits.UV_MIN, max=Limits.UV_MAX)

	# Last Measured Soil Temperature Value (Array)
	ST: Optional[list[Optional[float]]] = Field(description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=0, max_items=10, min=Limits.ST_MIN, max=Limits.ST_MAX)

	# Last Measured Soil Temperature Value (Single)
	ST_0: Optional[float] = Field(description="10 cm Soil temperature.", example=28.12)
	ST_1: Optional[float] = Field(description="20 cm Soil temperature.", example=27.12)
	ST_2: Optional[float] = Field(description="30 cm Soil temperature.", example=26.12)
	ST_3: Optional[float] = Field(description="40 cm Soil temperature.", example=25.12)
	ST_4: Optional[float] = Field(description="50 cm Soil temperature.", example=24.12)
	ST_5: Optional[float] = Field(description="60 cm Soil temperature.", example=23.12)
	ST_6: Optional[float] = Field(description="70 cm Soil temperature.", example=22.12)
	ST_7: Optional[float] = Field(description="80 cm Soil temperature.", example=21.12)
	ST_8: Optional[float] = Field(description="90 cm Soil temperature.", example=20.12)
	ST_9: Optional[float] = Field(description="100 cm Soil temperature.", example=19.12)

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23, min=Limits.R_MIN, max=Limits.R_MAX)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275, min=Limits.WD_MIN, max=Limits.WD_MAX)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25, min=Limits.WS_MIN, max=Limits.WS_MAX)

	# Instant Voltage Value
	V: Optional[list[Optional[float]]] = Field(description="Instant voltage measurement", example=[220.12, 222.12, 235.12, 225.12], min_items=0, max_items=4)
	V_R: Optional[float] = Field(description="Phase R instant voltage measurement", example=220.12)
	V_S: Optional[float] = Field(description="Phase S instant voltage measurement", example=220.12)
	V_T: Optional[float] = Field(description="Phase T instant voltage measurement", example=220.12)
	V_A: Optional[float] = Field(description="Instant voltage average measurement", example=220.12)

	# RMS Voltage Value
	VRMS: Optional[list[Optional[float]]] = Field(description="RMS voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VRMS_R: Optional[float] = Field(description="Phase R RMS voltage measurement", example=220.12)
	VRMS_S: Optional[float] = Field(description="Phase S RMS voltage measurement", example=220.12)
	VRMS_T: Optional[float] = Field(description="Phase T RMS voltage measurement", example=220.12)
	VRMS_A: Optional[float] = Field(description="RMS voltage average measurement", example=220.12)

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
	FQ: Optional[float] = Field(description="Frequency measurement", example=50.12)

	# Active Energy Value
	AE: Optional[list[Optional[float]]] = Field(description="Active energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	AE_R: Optional[float] = Field(description="Phase R active energy measurement", example=220.12)
	AE_S: Optional[float] = Field(description="Phase S active energy measurement", example=220.12)
	AE_T: Optional[float] = Field(description="Phase T active energy measurement", example=220.12)
	AE_A: Optional[float] = Field(description="Active energy average measurement", example=220.12)
	AE_TOT: Optional[float] = Field(description="Active energy total measurement", example=220.12)

	# Reactive Energy Leading Value
	RE_L: Optional[list[Optional[float]]] = Field(description="Reactive leading energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	RE_L_R: Optional[float] = Field(description="Phase R leading reactive energy measurement", example=220.12)
	RE_L_S: Optional[float] = Field(description="Phase S leading reactive energy measurement", example=220.12)
	RE_L_T: Optional[float] = Field(description="Phase T leading reactive energy measurement", example=220.12)
	RE_L_A: Optional[float] = Field(description="Reactive leading energy average measurement", example=220.12)
	RE_L_TOT: Optional[float] = Field(description="Total leading reactive energy measurement", example=220.12)

	# Reactive Energy Lagging Value
	RE_G: Optional[list[Optional[float]]] = Field(description="Reactive lagging energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	RE_G_R: Optional[float] = Field(description="Phase R lagging reactive energy measurement", example=220.12)
	RE_G_S: Optional[float] = Field(description="Phase S lagging reactive energy measurement", example=220.12)
	RE_G_T: Optional[float] = Field(description="Phase T lagging reactive energy measurement", example=220.12)
	RE_G_A: Optional[float] = Field(description="Reactive lagging energy average measurement", example=220.12)
	RE_G_TOT: Optional[float] = Field(description="Total lagging reactive energy measurement", example=220.12)

	# Max78630 Chip Temperature Value
	Max78630_T: Optional[float] = Field(description="Max78630 chip temperature measurement", example=20.12)

	# ST Root Validator
	@root_validator
	def Handle_ST_Fields(cls, Values):
		ST_Values = Values.get('ST')
		if ST_Values is not None:
			for i, Value in enumerate(ST_Values):
				Values[f'ST_{i}'] = Value
		else:
			pass
		return Values



# Define IoT RAW Data Base Model
# Model Version 01.03.00
class Data_Pack(CustomBaseModel):

	# Info
	Info: Info

	# Device
	Device: Device

	# Payload
	Payload: Payload
