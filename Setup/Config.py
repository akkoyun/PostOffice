# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from pydantic_settings import BaseSettings

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


# Service Settings
SERVER_NAME = 'PostOffice'

# Logging Settings
LOG_FILE = './Log/Service.LOG'