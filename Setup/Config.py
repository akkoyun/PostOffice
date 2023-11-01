# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from pydantic import BaseSettings

# Define Setting
class Settings(BaseSettings):

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

	# Kafka Consumer Group
	KAFKA_CONSUMER_GROUP: str

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