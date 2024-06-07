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

	# Load env File
	class Config:
		env_file = "Setup/.env"

# Set Setting
APP_Settings = Settings()