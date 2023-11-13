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

	# PCB Temperature Limits
	PCB_TEMPERATURE_MIN: float = -40.0
	PCB_TEMPERATURE_MAX: float = 85.0

	# PCB Humidity Limits
	PCB_HUMIDITY_MIN: float = 0.0
	PCB_HUMIDITY_MAX: float = 100.0

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


