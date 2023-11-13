# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from pydantic import BaseSettings

# Define Setting
class Settings(BaseSettings):

	# Server Settings
	SERVER_NAME: str

	# Logging Settings
	LOG_FILE: str

	# Database Settings
	DB_HOSTNAME: str
	DB_PORT: str
	DB_PASSWORD: str
	DB_NAME: str
	DB_USERNAME: str

	# Kafka Settings
	KAFKA_HOSTNAME: str
	KAFKA_PORT: int

	# Kafka Topics
	KAFKA_TOPIC_RAW: str
	KAFKA_TOPIC_PARAMETER: str
	KAFKA_TOPIC_PAYLOAD: str

	# Kafka Consumer Group
	KAFKA_CONSUMER_RAW_GROUP: str
	KAFKA_CONSUMER_PARAMETER_GROUP: str
	KAFKA_CONSUMER_PAYLOAD_GROUP: str

	# File Settings
	FILE_MANUFACTURER: str
	FILE_MODEL: str
	FILE_GSM_OPERATOR: str
	FILE_SIM: str
	FILE_MODEM: str
	FILE_DATA_SEGMENT: str
	FILE_MEASUREMENT_TYPE: str
	FILE_VERSION: str
	FILE_STATUS: str
	FILE_DEVICE: str

	# Load env File
	class Config:
		env_file = "Setup/.env"

# Set Setting
APP_Settings = Settings()

# Limit Settings
class Payload_Limits():

	# AT Limits
	AT_MIN: float = -40.0
	AT_MAX: float = 85.0
	
	# AH Limits
	AH_MIN: float = 0.0
	AH_MAX: float = 100.0

	# AP Limits
	AP_MIN: float = 500.0
	AP_MAX: float = 2000.0

	# VL Limits
	VL_MIN: float = 0.0
	VL_MAX: float = 100000.0

	# IR Limits
	IR_MIN: float = 0.0
	IR_MAX: float = 100000.0

	# UV Limits
	UV_MIN: float = 0.0
	UV_MAX: float = 12.0

	# ST Limits
	ST_MIN: float = -50.0
	ST_MAX: float = 100.0

	# R Limits
	R_MIN: float = 0.0
	R_MAX: float = 1024.0

	# WD Limits
	WD_MIN: float = 0.0
	WD_MAX: float = 360.0

	# WS Limits
	WS_MIN: float = 0.0
	WS_MAX: float = 255.0

	# Latitude Limits
	LATITUDE_MIN: float = -90.0
	LATITUDE_MAX: float = 90.0

	# Longitude Limits
	LONGITUDE_MIN: float = -180.0
	LONGITUDE_MAX: float = 180.0

	# TODO: Check Limits

	# Instant Voltage Limits
	INSTANT_VOLTAGE_MIN: float = -700.0
	INSTANT_VOLTAGE_MAX: float = 700.0

	# RMS Voltage Limits
	RMS_VOLTAGE_MIN: float = 0.0
	RMS_VOLTAGE_MAX: float = 700.0

	# Fundamental Voltage Limits
	FUNDAMENTAL_VOLTAGE_MIN: float = 0.0
	FUNDAMENTAL_VOLTAGE_MAX: float = 700.0

	# Harmonic Voltage Limits
	HARMONIC_VOLTAGE_MIN: float = 0.0
	HARMONIC_VOLTAGE_MAX: float = 700.0

	# Instant Current Limits
	INSTANT_CURRENT_MIN: float = -700.0
	INSTANT_CURRENT_MAX: float = 700.0

	# Peak Current Limits
	PEAK_CURRENT_MIN: float = 0.0
	PEAK_CURRENT_MAX: float = 700.0

	# RMS Current Limits
	RMS_CURRENT_MIN: float = 0.0
	RMS_CURRENT_MAX: float = 700.0

	# Fundamental Current Limits
	FUNDAMENTAL_CURRENT_MIN: float = 0.0
	FUNDAMENTAL_CURRENT_MAX: float = 700.0

	# Harmonic Current Limits
	HARMONIC_CURRENT_MIN: float = 0.0
	HARMONIC_CURRENT_MAX: float = 700.0

	# Active Power Limits
	ACTIVE_POWER_MIN: float = 0.0
	ACTIVE_POWER_MAX: float = 700.0

	# Reactive Power Limits
	REACTIVE_POWER_MIN: float = 0.0
	REACTIVE_POWER_MAX: float = 700.0

	# Apparent Power Limits
	APPARENT_POWER_MIN: float = 0.0
	APPARENT_POWER_MAX: float = 700.0

	# Fundamental Reactive Power Limits
	FUNDAMENTAL_REACTIVE_POWER_MIN: float = 0.0
	FUNDAMENTAL_REACTIVE_POWER_MAX: float = 700.0

	# Harmonic Reactive Power Limits
	HARMONIC_REACTIVE_POWER_MIN: float = 0.0
	HARMONIC_REACTIVE_POWER_MAX: float = 700.0

	# Fundamental Power Limits
	FUNDAMENTAL_POWER_MIN: float = 0.0
	FUNDAMENTAL_POWER_MAX: float = 700.0

	# Harmonic Power Limits
	HARMONIC_POWER_MIN: float = 0.0
	HARMONIC_POWER_MAX: float = 700.0

	# Fundamental Volt Ampere Limits
	FUNDAMENTAL_VOLT_AMPER_MIN: float = 0.0
	FUNDAMENTAL_VOLT_AMPER_MAX: float = 700.0

	# Power Factor Limits
	POWER_FACTOR_MIN: float = 0.0
	POWER_FACTOR_MAX: float = 700.0

	# Frequency Limits
	FREQUENCY_MIN: float = 0.0
	FREQUENCY_MAX: float = 700.0

	# Active Energy Limits
	ACTIVE_ENERGY_MIN: float = 0.0
	ACTIVE_ENERGY_MAX: float = 700.0

	# Reactive Energy Limits
	REACTIVE_ENERGY_MIN: float = 0.0
	REACTIVE_ENERGY_MAX: float = 700.0

	# Temperature Limits
	TEMPERATURE_MIN: float = 0.0
	TEMPERATURE_MAX: float = 700.0
