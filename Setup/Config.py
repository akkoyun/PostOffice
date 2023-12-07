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
	KAFKA_TOPIC_DISCORD: str

	# Kafka Consumer Group
	KAFKA_CONSUMER_RAW_GROUP: str
	KAFKA_CONSUMER_PARAMETER_GROUP: str
	KAFKA_CONSUMER_PAYLOAD_GROUP: str
	KAFKA_CONSUMER_DISCORD_GROUP: str

	# File Settings
	DATA_REPOSITORY: str
	FILE_MANUFACTURER: str
	FILE_MODEL: str
	FILE_PROJECT: str
	FILE_GSM_OPERATOR: str
	FILE_SIM: str
	FILE_MODEM: str
	FILE_DATA_SEGMENT: str
	FILE_MEASUREMENT_TYPE: str
	FILE_VERSION: str
	FILE_STATUS: str
	FILE_DEVICE: str
	FILE_CALIBRATION: str

	# Discord Settings
	DISCORD_TOKEN: str
	DISCORD_CHANNEL_ID: int

	# Load env File
	class Config:
		env_file = "Setup/.env"

# Set Setting
APP_Settings = Settings()
