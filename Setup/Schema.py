# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from Setup.Config import WeatherStat_Limits as Limits

# Define IoT Data Base Model
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

# Define WeatherStat payload
class Payload(BaseModel):

	# Latitude Value of Device
	Latitude: Optional[float] = Field(description="GNSS lattitude value.", example=1.243242342, min=-360, max=360)

	# Longitude Value of Device
	Longitude: Optional[float] = Field(description="GNSS longitude value.", example=23.3213232, min=-360, max=360)
    
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

	# Last Measured Soil Temperature Value
	ST: list[Optional[float]] = Field(description="Soil temperature.", example=[28.12, 27.12, 26.12, 25.12], min_items=0, max_items=10, min=Limits.ST_MIN, max=Limits.ST_MAX)

	# Last Measured Rain Value
	R: Optional[int] = Field(description="Rain tip counter.", example=23, min=Limits.R_MIN, max=Limits.R_MAX)

	# Last Measured Wind Direction Value
	WD: Optional[int] = Field(description="Wind direction.", example=275, min=Limits.WD_MIN, max=Limits.WD_MAX)

	# Last Measured Wind Speed Value
	WS: Optional[float] = Field(description="Wind speed.", example=25, min=Limits.WS_MIN, max=Limits.WS_MAX)

	# Instant Voltage Value
	V: list[Optional[float]] = Field(description="Instant voltage measurement", example=[220.12, 222.12, 235.12, 225.12], min_items=0, max_items=4)

	# Phase R Instant Voltage Value
	V_R: Optional[float] = Field(description="Phase R instant voltage measurement", example=220.12)

	# Phase S Instant Voltage Value
	V_S: Optional[float] = Field(description="Phase S instant voltage measurement", example=220.12)

	# Phase T Instant Voltage Value
	V_T: Optional[float] = Field(description="Phase T instant voltage measurement", example=220.12)

	# Instant Voltage Average Value
	V_A: Optional[float] = Field(description="Instant voltage average measurement", example=220.12)

	# RMS Voltage Value
	VRMS: list[Optional[float]] = Field(description="RMS voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R RMS Voltage Value
	VRMS_R: Optional[float] = Field(description="Phase R RMS voltage measurement", example=220.12)

	# Phase S RMS Voltage Value
	VRMS_S: Optional[float] = Field(description="Phase S RMS voltage measurement", example=220.12)

	# Phase T RMS Voltage Value
	VRMS_T: Optional[float] = Field(description="Phase T RMS voltage measurement", example=220.12)

	# RMS Voltage Average Value
	VRMS_A: Optional[float] = Field(description="RMS voltage average measurement", example=220.12)

	# Fundamental Voltage Value
	VF: list[Optional[float]] = Field(description="Fundamental voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Fundamental Voltage Value
	VF_R: Optional[float] = Field(description="Phase R fundamental voltage measurement", example=220.12)

	# Phase S Fundamental Voltage Value
	VF_S: Optional[float] = Field(description="Phase S fundamental voltage measurement", example=220.12)

	# Phase T Fundamental Voltage Value
	VF_T: Optional[float] = Field(description="Phase T fundamental voltage measurement", example=220.12)

	# Fundamental Voltage Average Value
	VF_A: Optional[float] = Field(description="Fundamental voltage average measurement", example=220.12)

	# Harmonic Voltage Value
	VH: list[Optional[float]] = Field(description="Harmonic voltage measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Harmonic Voltage Value
	VH_R: Optional[float] = Field(description="Phase R harmonic voltage measurement", example=220.12)

	# Phase S Harmonic Voltage Value
	VH_S: Optional[float] = Field(description="Phase S harmonic voltage measurement", example=220.12)

	# Phase T Harmonic Voltage Value
	VH_T: Optional[float] = Field(description="Phase T harmonic voltage measurement", example=220.12)

	# Harmonic Voltage Average Value
	VH_A: Optional[float] = Field(description="Harmonic voltage average measurement", example=220.12)

	# Instant Current Value
	I: list[Optional[float]] = Field(description="Instant current measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Instant Current Value
	I_R: Optional[float] = Field(description="Phase R instant current measurement", example=20.12)

	# Phase S Instant Current Value
	I_S: Optional[float] = Field(description="Phase S instant current measurement", example=20.12)

	# Phase T Instant Current Value
	I_T: Optional[float] = Field(description="Phase T instant current measurement", example=20.12)

	# Instant Current Average Value
	I_A: Optional[float] = Field(description="Instant current average measurement", example=20.12)

	# Peak Current Value
	IP: list[Optional[float]] = Field(description="Peak current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)

	# Phase R Peak Current Value
	IP_R: Optional[float] = Field(description="Phase R peak current measurement", example=20.12)

	# Phase S Peak Current Value
	IP_S: Optional[float] = Field(description="Phase S peak current measurement", example=20.12)

	# Phase T Peak Current Value
	IP_T: Optional[float] = Field(description="Phase T peak current measurement", example=20.12)

	# Peak Current Average Value
	IP_A: Optional[float] = Field(description="Peak current average measurement", example=20.12)

	# RMS Current Value
	IRMS: list[Optional[float]] = Field(description="RMS current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)

	# Phase R RMS Current Value
	IRMS_R: Optional[float] = Field(description="Phase R RMS current measurement", example=20.12)

	# Phase S RMS Current Value
	IRMS_S: Optional[float] = Field(description="Phase S RMS current measurement", example=20.12)

	# Phase T RMS Current Value
	IRMS_T: Optional[float] = Field(description="Phase T RMS current measurement", example=20.12)

	# RMS Current Average Value
	IRMS_A: Optional[float] = Field(description="RMS current average measurement", example=20.12)

	# Fundamental Current Value
	IF: list[Optional[float]] = Field(description="Fundamental current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)

	# Phase R Fundamental Current Value
	IF_R: Optional[float] = Field(description="Phase R fundamental current measurement", example=20.12)

	# Phase S Fundamental Current Value
	IF_S: Optional[float] = Field(description="Phase S fundamental current measurement", example=20.12)

	# Phase T Fundamental Current Value
	IF_T: Optional[float] = Field(description="Phase T fundamental current measurement", example=20.12)

	# Fundamental Current Average Value
	IF_A: Optional[float] = Field(description="Fundamental current average measurement", example=20.12)

	# Harmonic Current Value
	IH: list[Optional[float]] = Field(description="Harmonic current measurement", example=[20.12, 21.12, 19.12, 20.12], min_items=0, max_items=4)

	# Phase R Harmonic Current Value
	IH_R: Optional[float] = Field(description="Phase R harmonic current measurement", example=20.12)

	# Phase S Harmonic Current Value
	IH_S: Optional[float] = Field(description="Phase S harmonic current measurement", example=20.12)

	# Phase T Harmonic Current Value
	IH_T: Optional[float] = Field(description="Phase T harmonic current measurement", example=20.12)

	# Harmonic Current Average Value
	IH_A: Optional[float] = Field(description="Harmonic current average measurement", example=20.12)

	# Active Power Value
	P: list[Optional[float]] = Field(description="Active power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Active Power Value
	P_R: Optional[float] = Field(description="Phase R active power measurement", example=220.12)

	# Phase S Active Power Value
	P_S: Optional[float] = Field(description="Phase S active power measurement", example=220.12)

	# Phase T Active Power Value
	P_T: Optional[float] = Field(description="Phase T active power measurement", example=220.12)

	# Active Power Average Value
	P_A: Optional[float] = Field(description="Active power average measurement", example=220.12)

	# Reactive Power Value
	Q: list[Optional[float]] = Field(description="Reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Reactive Power Value
	Q_R: Optional[float] = Field(description="Phase R reactive power measurement", example=220.12)

	# Phase S Reactive Power Value
	Q_S: Optional[float] = Field(description="Phase S reactive power measurement", example=220.12)

	# Phase T Reactive Power Value
	Q_T: Optional[float] = Field(description="Phase T reactive power measurement", example=220.12)

	# Reactive Power Average Value
	Q_A: Optional[float] = Field(description="Reactive power average measurement", example=220.12)

	# Apparent Power Value
	S: list[Optional[float]] = Field(description="Apparent power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Apparent Power Value
	S_R: Optional[float] = Field(description="Phase R apparent power measurement", example=220.12)

	# Phase S Apparent Power Value
	S_S: Optional[float] = Field(description="Phase S apparent power measurement", example=220.12)

	# Phase T Apparent Power Value
	S_T: Optional[float] = Field(description="Phase T apparent power measurement", example=220.12)

	# Apparent Power Average Value
	S_A: Optional[float] = Field(description="Apparent power average measurement", example=220.12)

	# Fundamental Reactive Power Value
	QFun: list[Optional[float]] = Field(description="Fundamental reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Fundamental Reactive Power Value
	QFun_R: Optional[float] = Field(description="Phase R fundamental reactive power measurement", example=220.12)

	# Phase S Fundamental Reactive Power Value
	QFun_S: Optional[float] = Field(description="Phase S fundamental reactive power measurement", example=220.12)

	# Phase T Fundamental Reactive Power Value
	QFun_T: Optional[float] = Field(description="Phase T fundamental reactive power measurement", example=220.12)

	# Fundamental Reactive Power Average Value
	QFun_A: Optional[float] = Field(description="Fundamental reactive power average measurement", example=220.12)

	# Harmonic Reactive Power Value
	QHarm: list[Optional[float]] = Field(description="Harmonic reactive power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Harmonic Reactive Power Value
	QHarm_R: Optional[float] = Field(description="Phase R harmonic reactive power measurement", example=220.12)

	# Phase S Harmonic Reactive Power Value
	QHarm_S: Optional[float] = Field(description="Phase S harmonic reactive power measurement", example=220.12)

	# Phase T Harmonic Reactive Power Value
	QHarm_T: Optional[float] = Field(description="Phase T harmonic reactive power measurement", example=220.12)

	# Harmonic Reactive Power Average Value
	QHarm_A: Optional[float] = Field(description="Harmonic reactive power average measurement", example=220.12)

	# Fundamental Power Value
	PFun: list[Optional[float]] = Field(description="Fundamental power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Fundamental Power Value
	PFun_R: Optional[float] = Field(description="Phase R fundamental power measurement", example=220.12)

	# Phase S Fundamental Power Value
	PFun_S: Optional[float] = Field(description="Phase S fundamental power measurement", example=220.12)

	# Phase T Fundamental Power Value
	PFun_T: Optional[float] = Field(description="Phase T fundamental power measurement", example=220.12)

	# Fundamental Power Average Value
	PFun_A: Optional[float] = Field(description="Fundamental power average measurement", example=220.12)

	# Harmonic Power Value
	PHar: list[Optional[float]] = Field(description="Harmonic power measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Harmonic Power Value
	PHar_R: Optional[float] = Field(description="Phase R harmonic power measurement", example=220.12)

	# Phase S Harmonic Power Value
	PHar_S: Optional[float] = Field(description="Phase S harmonic power measurement", example=220.12)

	# Phase T Harmonic Power Value
	PHar_T: Optional[float] = Field(description="Phase T harmonic power measurement", example=220.12)

	# Harmonic Power Average Value
	PHar_A: Optional[float] = Field(description="Harmonic power average measurement", example=220.12)

	# Fundamental Volt Amper 
	FunVA: list[Optional[float]] = Field(description="Fundamental volt ampere measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Fundamental Volt Amper
	FunVA_R: Optional[float] = Field(description="Phase R fundamental volt ampere measurement", example=220.12)

	# Phase S Fundamental Volt Amper
	FunVA_S: Optional[float] = Field(description="Phase S fundamental volt ampere measurement", example=220.12)

	# Phase T Fundamental Volt Amper
	FunVA_T: Optional[float] = Field(description="Phase T fundamental volt ampere measurement", example=220.12)

	# Fundamental Volt Amper Average
	FunVA_A: Optional[float] = Field(description="Fundamental volt ampere average measurement", example=220.12)

	# Power Factor Value
	PF: list[Optional[float]] = Field(description="Power factor measurement", example=[0.812, 0.812, 0.812, 0.812], min_items=0, max_items=4)

	# Phase R Power Factor Value
	PF_R: Optional[float] = Field(description="Phase R power factor measurement", example=0.81)

	# Phase S Power Factor Value
	PF_S: Optional[float] = Field(description="Phase S power factor measurement", example=0.81)

	# Phase T Power Factor Value
	PF_T: Optional[float] = Field(description="Phase T power factor measurement", example=0.81)

	# Power Factor Average Value
	PF_A: Optional[float] = Field(description="Power factor average measurement", example=0.81)

	# Frequency Value
	FQ: Optional[float] = Field(description="Frequency measurement", example=50.12)

	# Active Energy Value
	AE: list[Optional[float]] = Field(description="Active energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Active Energy Value
	AE_R: Optional[float] = Field(description="Phase R active energy measurement", example=220.12)

	# Phase S Active Energy Value
	AE_S: Optional[float] = Field(description="Phase S active energy measurement", example=220.12)

	# Phase T Active Energy Value
	AE_T: Optional[float] = Field(description="Phase T active energy measurement", example=220.12)

	# Active Energy Average Value
	AE_A: Optional[float] = Field(description="Active energy average measurement", example=220.12)

	# Reactive Energy Leading Value
	RE_L: list[Optional[float]] = Field(description="Reactive leading energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Reactive Energy Value
	RE_L_R: Optional[float] = Field(description="Phase R leading reactive energy measurement", example=220.12)

	# Phase S Reactive Energy Value
	RE_L_S: Optional[float] = Field(description="Phase S leading reactive energy measurement", example=220.12)

	# Phase T Reactive Energy Value
	RE_L_T: Optional[float] = Field(description="Phase T leading reactive energy measurement", example=220.12)

	# Reactive Energy Average Value
	RE_L_A: Optional[float] = Field(description="Reactive leading energy average measurement", example=220.12)

	# Total Leading Reactive Energy Value
	RE_L_TOT: Optional[float] = Field(description="Total leading reactive energy measurement", example=220.12)

	# Reactive Energy Lagging Value
	RE_G: list[Optional[float]] = Field(description="Reactive lagging energy measurement", example=[220.12, 221.12, 219.12, 220.12], min_items=0, max_items=4)

	# Phase R Reactive Energy Value
	RE_G_R: Optional[float] = Field(description="Phase R lagging reactive energy measurement", example=220.12)

	# Phase S Reactive Energy Value
	RE_G_S: Optional[float] = Field(description="Phase S lagging reactive energy measurement", example=220.12)

	# Phase T Reactive Energy Value
	RE_G_T: Optional[float] = Field(description="Phase T lagging reactive energy measurement", example=220.12)

	# Reactive Energy Average Value
	RE_G_A: Optional[float] = Field(description="Reactive lagging energy average measurement", example=220.12)

	# Total Lagging Reactive Energy Value
	RE_G_TOT: Optional[float] = Field(description="Total lagging reactive energy measurement", example=220.12)

	# Max78630 Chip Temperature Value
	Max78630_T: Optional[float] = Field(description="Max78630 chip temperature measurement", example=20.12)

# Define IoT RAW Data Base Model
# WeatherStat Model Version 01.03.00
class Data_Pack(BaseModel):

	# Info
	Info: Info

	# Device
	Device: Device

	# WeatherStat Payload
	Payload: Payload
