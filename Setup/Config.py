# Import Libraries
from pydantic import BaseSettings

# Define Setting
class Settings(BaseSettings):

	# Kafka Settings
	POSTOFFICE_KAFKA_HOSTNAME: str
	POSTOFFICE_KAFKA_PORT: str

	# Load env File
	class Config:
		env_file = "Setup/.env"

# Set Setting
APP_Settings = Settings()
