# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
from datetime import datetime
import re

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
	Latitude: Optional[float] = Field(description="GNSS lattitude value.", example=1.243242342)

	# Longitude Value of Device
	Longitude: Optional[float] = Field(description="GNSS longitude value.", example=23.3213232)

	# Last Measured PCB Temperature Value
	PCB_T: Optional[float] = Field(description="PCB temperature.", example=28.3232)

	# Last Measured PCB Humidity Value
	PCB_H: Optional[float] = Field(description="PCB humidity.", example=85.2332)

	# Last Measured Air Temperature Value
	AT: Optional[float] = Field(description="Air temperature.", example=28.3232)

	# Last Measured Relative Humidity Value
	AH: Optional[float] = Field(description="Air humidity.", example=85.2332)

	# Last Measured Air Pressure Value
	AP: Optional[float] = Field(description="Air pressure.", example=985.55)

	# Last Measured Visual Light Value
	VL: Optional[int] = Field(description="Visual light.", example=1234)

	# Last Measured Infrared Light Value
	IR: Optional[int] = Field(description="Infrared light.", example=1234)

	# Last Measured UV Value
	UV: Optional[float] = Field(description="UV index.", example=2.12)

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

	# ST Root Validator
	@root_validator
	def Handle_ST_Fields(cls, Values):
		ST_Values = Values.get('ST')
		if ST_Values is not None:
			for i, Value in enumerate(ST_Values):
				if i == 0: Values['ST0'] = Value
				if i == 1: Values['ST1'] = Value
				if i == 2: Values['ST2'] = Value
				if i == 3: Values['ST3'] = Value
				if i == 4: Values['ST4'] = Value
				if i == 5: Values['ST5'] = Value
				if i == 6: Values['ST6'] = Value
				if i == 7: Values['ST7'] = Value
				if i == 8: Values['ST8'] = Value
				if i == 9: Values['ST9'] = Value
		else:
			pass
		return Values

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25)

	# Instant Voltage Value
	V: Optional[list[Optional[float]]] = Field(description="Instant voltage measurement", example=[220.12, 222.12, 235.12, 225.12], min_items=0, max_items=4)
	V_R: Optional[float] = Field(description="Phase R instant voltage measurement", example=220.12)
	V_S: Optional[float] = Field(description="Phase S instant voltage measurement", example=220.12)
	V_T: Optional[float] = Field(description="Phase T instant voltage measurement", example=220.12)
	V_A: Optional[float] = Field(description="Instant voltage average measurement", example=220.12)

	# V Root Validator
	@root_validator
	def Handle_V_Fields(cls, Values):
		V_Values = Values.get('V')
		if V_Values is not None:
			for i, Value in enumerate(V_Values):
				if i == 0: Values['V_R'] = Value
				if i == 1: Values['V_S'] = Value
				if i == 2: Values['V_T'] = Value
				if i == 3: Values['V_A'] = Value
		else:
			pass
		return Values

	# RMS Voltage Value
	VRMS: Optional[list[Optional[float]]] = Field(description="RMS voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VRMS_R: Optional[float] = Field(description="Phase R RMS voltage measurement", example=220.12)
	VRMS_S: Optional[float] = Field(description="Phase S RMS voltage measurement", example=220.12)
	VRMS_T: Optional[float] = Field(description="Phase T RMS voltage measurement", example=220.12)
	VRMS_A: Optional[float] = Field(description="RMS voltage average measurement", example=220.12)

	# VRMS Root Validator
	@root_validator
	def Handle_VRMS_Fields(cls, Values):
		VRMS_Values = Values.get('VRMS')
		if VRMS_Values is not None:
			for i, Value in enumerate(VRMS_Values):
				if i == 0: Values['VRMS_R'] = Value
				if i == 1: Values['VRMS_S'] = Value
				if i == 2: Values['VRMS_T'] = Value
				if i == 3: Values['VRMS_A'] = Value
		else:
			pass
		return Values

	# Fundamental Voltage Value
	VFun: Optional[list[Optional[float]]] = Field(description="Fundamental voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VFun_R: Optional[float] = Field(description="Phase R fundamental voltage measurement", example=220.12)
	VFun_S: Optional[float] = Field(description="Phase S fundamental voltage measurement", example=220.12)
	VFun_T: Optional[float] = Field(description="Phase T fundamental voltage measurement", example=220.12)
	VFun_A: Optional[float] = Field(description="Fundamental voltage average measurement", example=220.12)

	# VFun Root Validator
	@root_validator
	def Handle_VFun_Fields(cls, Values):
		VFun_Values = Values.get('VFun')
		if VFun_Values is not None:
			for i, Value in enumerate(VFun_Values):
				if i == 0: Values['VFun_R'] = Value
				if i == 1: Values['VFun_S'] = Value
				if i == 2: Values['VFun_T'] = Value
				if i == 3: Values['VFun_A'] = Value
		else:
			pass
		return Values

	# Harmonic Voltage Value
	VHarm: Optional[list[Optional[float]]] = Field(description="Harmonic voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	VHarm_R: Optional[float] = Field(description="Phase R harmonic voltage measurement", example=220.12)
	VHarm_S: Optional[float] = Field(description="Phase S harmonic voltage measurement", example=220.12)
	VHarm_T: Optional[float] = Field(description="Phase T harmonic voltage measurement", example=220.12)
	VHarm_A: Optional[float] = Field(description="Harmonic voltage average measurement", example=220.12)

	# Frequency Value
	FQ: Optional[float] = Field(description="Frequency measurement", example=50.12)

	# VHarm Root Validator
	@root_validator
	def Handle_VHarm_Fields(cls, Values):
		VHarm_Values = Values.get('VHarm')
		if VHarm_Values is not None:
			for i, Value in enumerate(VHarm_Values):
				if i == 0: Values['VHarm_R'] = Value
				if i == 1: Values['VHarm_S'] = Value
				if i == 2: Values['VHarm_T'] = Value
				if i == 3: Values['VHarm_A'] = Value
		else:
			pass
		return Values

	# Instant Current Value
	I: Optional[list[Optional[float]]] = Field(description="Instant current measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	I_R: Optional[float] = Field(description="Phase R instant current measurement", example=20.12)
	I_S: Optional[float] = Field(description="Phase S instant current measurement", example=20.12)
	I_T: Optional[float] = Field(description="Phase T instant current measurement", example=20.12)
	I_A: Optional[float] = Field(description="Instant current average measurement", example=20.12)

	# I Root Validator
	@root_validator
	def Handle_I_Fields(cls, Values):
		I_Values = Values.get('I')
		if I_Values is not None:
			for i, Value in enumerate(I_Values):
				if i == 0: Values['I_R'] = Value
				if i == 1: Values['I_S'] = Value
				if i == 2: Values['I_T'] = Value
				if i == 3: Values['I_A'] = Value
		else:
			pass
		return Values

	# Peak Current Value
	IP: Optional[list[Optional[float]]] = Field(description="Peak current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IP_R: Optional[float] = Field(description="Phase R peak current measurement", example=20.12)
	IP_S: Optional[float] = Field(description="Phase S peak current measurement", example=20.12)
	IP_T: Optional[float] = Field(description="Phase T peak current measurement", example=20.12)
	IP_A: Optional[float] = Field(description="Peak current average measurement", example=20.12)

	# IP Root Validator
	@root_validator
	def Handle_IP_Fields(cls, Values):
		IP_Values = Values.get('IP')
		if IP_Values is not None:
			for i, Value in enumerate(IP_Values):
				if i == 0: Values['IP_R'] = Value
				if i == 1: Values['IP_S'] = Value
				if i == 2: Values['IP_T'] = Value
				if i == 3: Values['IP_A'] = Value
		else:
			pass
		return Values

	# RMS Current Value
	IRMS: Optional[list[Optional[float]]] = Field(description="RMS current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IRMS_R: Optional[float] = Field(description="Phase R RMS current measurement", example=20.12)
	IRMS_S: Optional[float] = Field(description="Phase S RMS current measurement", example=20.12)
	IRMS_T: Optional[float] = Field(description="Phase T RMS current measurement", example=20.12)
	IRMS_A: Optional[float] = Field(description="RMS current average measurement", example=20.12)

	# IRMS Root Validator
	@root_validator
	def Handle_IRMS_Fields(cls, Values):
		IRMS_Values = Values.get('IRMS')
		if IRMS_Values is not None:
			for i, Value in enumerate(IRMS_Values):
				if i == 0: Values['IRMS_R'] = Value
				if i == 1: Values['IRMS_S'] = Value
				if i == 2: Values['IRMS_T'] = Value
				if i == 3: Values['IRMS_A'] = Value
		else:
			pass
		return Values

	# Fundamental Current Value
	IFun: Optional[list[Optional[float]]] = Field(description="Fundamental current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IFun_R: Optional[float] = Field(description="Phase R fundamental current measurement", example=20.12)
	IFun_S: Optional[float] = Field(description="Phase S fundamental current measurement", example=20.12)
	IFun_T: Optional[float] = Field(description="Phase T fundamental current measurement", example=20.12)
	IFun_A: Optional[float] = Field(description="Fundamental current average measurement", example=20.12)

	# IFun Root Validator
	@root_validator
	def Handle_IFun_Fields(cls, Values):
		IFun_Values = Values.get('IFun')
		if IFun_Values is not None:
			for i, Value in enumerate(IFun_Values):
				if i == 0: Values['IFun_R'] = Value
				if i == 1: Values['IFun_S'] = Value
				if i == 2: Values['IFun_T'] = Value
				if i == 3: Values['IFun_A'] = Value
		else:
			pass
		return Values

	# Harmonic Current Value
	IHarm: Optional[list[Optional[float]]] = Field(description="Harmonic current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)
	IHarm_R: Optional[float] = Field(description="Phase R harmonic current measurement", example=20.12)
	IHarm_S: Optional[float] = Field(description="Phase S harmonic current measurement", example=20.12)
	IHarm_T: Optional[float] = Field(description="Phase T harmonic current measurement", example=20.12)
	IHarm_A: Optional[float] = Field(description="Harmonic current average measurement", example=20.12)

	# IHarm Root Validator
	@root_validator
	def Handle_IHarm_Fields(cls, Values):
		IHarm_Values = Values.get('IHarm')
		if IHarm_Values is not None:
			for i, Value in enumerate(IHarm_Values):
				if i == 0: Values['IHarm_R'] = Value
				if i == 1: Values['IHarm_S'] = Value
				if i == 2: Values['IHarm_T'] = Value
				if i == 3: Values['IHarm_A'] = Value
		else:
			pass
		return Values

	# Active Power Value
	P: Optional[list[Optional[float]]] = Field(description="Active power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	P_R: Optional[float] = Field(description="Phase R active power measurement", example=220.12)
	P_S: Optional[float] = Field(description="Phase S active power measurement", example=220.12)
	P_T: Optional[float] = Field(description="Phase T active power measurement", example=220.12)
	P_A: Optional[float] = Field(description="Active power average measurement", example=220.12)

	# P Root Validator
	@root_validator
	def Handle_P_Fields(cls, Values):
		P_Values = Values.get('P')
		if P_Values is not None:
			for i, Value in enumerate(P_Values):
				if i == 0: Values['P_R'] = Value
				if i == 1: Values['P_S'] = Value
				if i == 2: Values['P_T'] = Value
				if i == 3: Values['P_A'] = Value
		else:
			pass
		return Values

	# Reactive Power Value
	Q: Optional[list[Optional[float]]] = Field(description="Reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	Q_R: Optional[float] = Field(description="Phase R reactive power measurement", example=220.12)
	Q_S: Optional[float] = Field(description="Phase S reactive power measurement", example=220.12)
	Q_T: Optional[float] = Field(description="Phase T reactive power measurement", example=220.12)
	Q_A: Optional[float] = Field(description="Reactive power average measurement", example=220.12)

	# Q Root Validator
	@root_validator
	def Handle_Q_Fields(cls, Values):
		Q_Values = Values.get('Q')
		if Q_Values is not None:
			for i, Value in enumerate(Q_Values):
				if i == 0: Values['Q_R'] = Value
				if i == 1: Values['Q_S'] = Value
				if i == 2: Values['Q_T'] = Value
				if i == 3: Values['Q_A'] = Value
		else:
			pass
		return Values

	# Apparent Power Value
	S: Optional[list[Optional[float]]] = Field(description="Apparent power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	S_R: Optional[float] = Field(description="Phase R apparent power measurement", example=220.12)
	S_S: Optional[float] = Field(description="Phase S apparent power measurement", example=220.12)
	S_T: Optional[float] = Field(description="Phase T apparent power measurement", example=220.12)
	S_A: Optional[float] = Field(description="Apparent power average measurement", example=220.12)

	# S Root Validator
	@root_validator
	def Handle_S_Fields(cls, Values):
		S_Values = Values.get('S')
		if S_Values is not None:
			for i, Value in enumerate(S_Values):
				if i == 0: Values['S_R'] = Value
				if i == 1: Values['S_S'] = Value
				if i == 2: Values['S_T'] = Value
				if i == 3: Values['S_A'] = Value
		else:
			pass
		return Values

	# Fundamental Reactive Power Value
	QFun: Optional[list[Optional[float]]] = Field(description="Fundamental reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	QFun_R: Optional[float] = Field(description="Phase R fundamental reactive power measurement", example=220.12)
	QFun_S: Optional[float] = Field(description="Phase S fundamental reactive power measurement", example=220.12)
	QFun_T: Optional[float] = Field(description="Phase T fundamental reactive power measurement", example=220.12)
	QFun_A: Optional[float] = Field(description="Fundamental reactive power average measurement", example=220.12)

	# QFun Root Validator
	@root_validator
	def Handle_QFun_Fields(cls, Values):
		QFun_Values = Values.get('QFun')
		if QFun_Values is not None:
			for i, Value in enumerate(QFun_Values):
				if i == 0: Values['QFun_R'] = Value
				if i == 1: Values['QFun_S'] = Value
				if i == 2: Values['QFun_T'] = Value
				if i == 3: Values['QFun_A'] = Value
		else:
			pass
		return Values

	# Harmonic Reactive Power Value
	QHarm: Optional[list[Optional[float]]] = Field(description="Harmonic reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	QHarm_R: Optional[float] = Field(description="Phase R harmonic reactive power measurement", example=220.12)
	QHarm_S: Optional[float] = Field(description="Phase S harmonic reactive power measurement", example=220.12)
	QHarm_T: Optional[float] = Field(description="Phase T harmonic reactive power measurement", example=220.12)
	QHarm_A: Optional[float] = Field(description="Harmonic reactive power average measurement", example=220.12)

	# QHarm Root Validator
	@root_validator
	def Handle_QHarm_Fields(cls, Values):
		QHarm_Values = Values.get('QHarm')
		if QHarm_Values is not None:
			for i, Value in enumerate(QHarm_Values):
				if i == 0: Values['QHarm_R'] = Value
				if i == 1: Values['QHarm_S'] = Value
				if i == 2: Values['QHarm_T'] = Value
				if i == 3: Values['QHarm_A'] = Value
		else:
			pass
		return Values

	# Fundamental Power Value
	PFun: Optional[list[Optional[float]]] = Field(description="Fundamental power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	PFun_R: Optional[float] = Field(description="Phase R fundamental power measurement", example=220.12)
	PFun_S: Optional[float] = Field(description="Phase S fundamental power measurement", example=220.12)
	PFun_T: Optional[float] = Field(description="Phase T fundamental power measurement", example=220.12)
	PFun_A: Optional[float] = Field(description="Fundamental power average measurement", example=220.12)

	# PFun Root Validator
	@root_validator
	def Handle_PFun_Fields(cls, Values):
		PFun_Values = Values.get('PFun')
		if PFun_Values is not None:
			for i, Value in enumerate(PFun_Values):
				if i == 0: Values['PFun_R'] = Value
				if i == 1: Values['PFun_S'] = Value
				if i == 2: Values['PFun_T'] = Value
				if i == 3: Values['PFun_A'] = Value
		else:
			pass
		return Values

	# Harmonic Power Value
	PHarm: Optional[list[Optional[float]]] = Field(description="Harmonic power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	PHarm_R: Optional[float] = Field(description="Phase R harmonic power measurement", example=220.12)
	PHarm_S: Optional[float] = Field(description="Phase S harmonic power measurement", example=220.12)
	PHarm_T: Optional[float] = Field(description="Phase T harmonic power measurement", example=220.12)
	PHarm_A: Optional[float] = Field(description="Harmonic power average measurement", example=220.12)

	# PHarm Root Validator
	@root_validator
	def Handle_PHarm_Fields(cls, Values):
		PHarm_Values = Values.get('PHarm')
		if PHarm_Values is not None:
			for i, Value in enumerate(PHarm_Values):
				if i == 0: Values['PHarm_R'] = Value
				if i == 1: Values['PHarm_S'] = Value
				if i == 2: Values['PHarm_T'] = Value
				if i == 3: Values['PHarm_A'] = Value
		else:
			pass
		return Values

	# Fundamental Volt Amper 
	FunVA: Optional[list[Optional[float]]] = Field(description="Fundamental volt ampere measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)
	FunVA_R: Optional[float] = Field(description="Phase R fundamental volt ampere measurement", example=220.12)
	FunVA_S: Optional[float] = Field(description="Phase S fundamental volt ampere measurement", example=220.12)
	FunVA_T: Optional[float] = Field(description="Phase T fundamental volt ampere measurement", example=220.12)
	FunVA_A: Optional[float] = Field(description="Fundamental volt ampere average measurement", example=220.12)

	# FunVA Root Validator
	@root_validator
	def Handle_FunVA_Fields(cls, Values):
		FunVA_Values = Values.get('FunVA')
		if FunVA_Values is not None:
			for i, Value in enumerate(FunVA_Values):
				if i == 0: Values['FunVA_R'] = Value
				if i == 1: Values['FunVA_S'] = Value
				if i == 2: Values['FunVA_T'] = Value
				if i == 3: Values['FunVA_A'] = Value
		else:
			pass
		return Values

	# Power Factor Value
	PF: Optional[list[Optional[float]]] = Field(description="Power factor measurement", example=[0.812, 0.812, 0.812, 0.812], min_items=0, max_items=4)
	PF_R: Optional[float] = Field(description="Phase R power factor measurement", example=0.81)
	PF_S: Optional[float] = Field(description="Phase S power factor measurement", example=0.81)
	PF_T: Optional[float] = Field(description="Phase T power factor measurement", example=0.81)
	PF_A: Optional[float] = Field(description="Power factor average measurement", example=0.81)

	# PF Root Validator
	@root_validator
	def Handle_PF_Fields(cls, Values):
		PF_Values = Values.get('PF')
		if PF_Values is not None:
			for i, Value in enumerate(PF_Values):
				if i == 0: Values['PF_R'] = Value
				if i == 1: Values['PF_S'] = Value
				if i == 2: Values['PF_T'] = Value
				if i == 3: Values['PF_A'] = Value
		else:
			pass
		return Values

	# Active Energy Value
	AE: Optional[list[Optional[float]]] = Field(description="Active energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	AE_R: Optional[float] = Field(description="Phase R active energy measurement", example=220.12)
	AE_S: Optional[float] = Field(description="Phase S active energy measurement", example=220.12)
	AE_T: Optional[float] = Field(description="Phase T active energy measurement", example=220.12)
	AE_A: Optional[float] = Field(description="Active energy average measurement", example=220.12)
	AE_TOT: Optional[float] = Field(description="Active energy total measurement", example=220.12)

	# AE Root Validator
	@root_validator
	def Handle_AE_Fields(cls, Values):
		AE_Values = Values.get('AE')
		if AE_Values is not None:
			for i, Value in enumerate(AE_Values):
				if i == 0: Values['AE_R'] = Value
				if i == 1: Values['AE_S'] = Value
				if i == 2: Values['AE_T'] = Value
				if i == 3: Values['AE_A'] = Value
				if i == 4: Values['AE_TOT'] = Value
		else:
			pass
		return Values

	# Reactive Energy Leading Value
	RE_L: Optional[list[Optional[float]]] = Field(description="Reactive leading energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	RE_L_R: Optional[float] = Field(description="Phase R leading reactive energy measurement", example=220.12)
	RE_L_S: Optional[float] = Field(description="Phase S leading reactive energy measurement", example=220.12)
	RE_L_T: Optional[float] = Field(description="Phase T leading reactive energy measurement", example=220.12)
	RE_L_A: Optional[float] = Field(description="Reactive leading energy average measurement", example=220.12)
	RE_L_TOT: Optional[float] = Field(description="Total leading reactive energy measurement", example=220.12)

	# RE_L Root Validator
	@root_validator
	def Handle_RE_L_Fields(cls, Values):
		RE_L_Values = Values.get('RE_L')
		if RE_L_Values is not None:
			for i, Value in enumerate(RE_L_Values):
				if i == 0: Values['RE_L_R'] = Value
				if i == 1: Values['RE_L_S'] = Value
				if i == 2: Values['RE_L_T'] = Value
				if i == 3: Values['RE_L_A'] = Value
				if i == 4: Values['RE_L_TOT'] = Value
		else:
			pass
		return Values

	# Reactive Energy Lagging Value
	RE_G: Optional[list[Optional[float]]] = Field(description="Reactive lagging energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=5)
	RE_G_R: Optional[float] = Field(description="Phase R lagging reactive energy measurement", example=220.12)
	RE_G_S: Optional[float] = Field(description="Phase S lagging reactive energy measurement", example=220.12)
	RE_G_T: Optional[float] = Field(description="Phase T lagging reactive energy measurement", example=220.12)
	RE_G_A: Optional[float] = Field(description="Reactive lagging energy average measurement", example=220.12)
	RE_G_TOT: Optional[float] = Field(description="Total lagging reactive energy measurement", example=220.12)

	# RE_G Root Validator
	@root_validator
	def Handle_RE_G_Fields(cls, Values):
		RE_G_Values = Values.get('RE_G')
		if RE_G_Values is not None:
			for i, Value in enumerate(RE_G_Values):
				if i == 0: Values['RE_G_R'] = Value
				if i == 1: Values['RE_G_S'] = Value
				if i == 2: Values['RE_G_T'] = Value
				if i == 3: Values['RE_G_A'] = Value
				if i == 4: Values['RE_G_TOT'] = Value
		else:
			pass
		return Values

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
