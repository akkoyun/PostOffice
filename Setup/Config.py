# Import Libraries
from pydantic import BaseSettings

# Define Setting
class Settings(BaseSettings):

	# Logging Settings
	POSTOFFICE_LOG_FILE: str

	# Database Settings
	POSTOFFICE_DB_HOSTNAME: str
	POSTOFFICE_DB_PORT: str
	POSTOFFICE_DB_PASSWORD: str
	POSTOFFICE_DB_NAME: str
	POSTOFFICE_DB_USERNAME: str

	# Load env File
	class Config:
		env_file = "Setup/.env"

# Set Setting
APP_Settings = Settings()