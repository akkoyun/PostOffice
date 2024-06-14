# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from pydantic import BaseSettings, ConfigDict

# Define Setting
class Settings(BaseSettings):

    # Server Settings
    SERVER_NAME: str
    PROJECT_ROOT: str

    # Logging Settings
    LOG_FILE: str
    LOG_DIR: str
    LOG_SERVICE_ERROR: str
    LOG_SERVICE_ACCESS: str

    # Database Settings
    DB_HOSTNAME: str
    DB_PORT: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str

    # File Settings
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

    # Load env File
    Config = ConfigDict(env_file="Setup/.env")

# Set Setting
APP_Settings = Settings()
