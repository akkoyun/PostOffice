from pydantic import BaseSettings

# Define Setting
class Settings(BaseSettings):

	POSTOFFICE_DB_HOSTNAME: str
	POSTOFFICE_DB_PORT: str
	POSTOFFICE_DB_PASSWORD: str
	POSTOFFICE_DB_NAME: str
	POSTOFFICE_DB_USERNAME: str

	KAFKA_HOSTNAME: str
	KAFKA_PORT: str
	KAFKA_TOPIC_RAW: str

	class Config:
		env_file = ".env"

# Set Setting
APP_Settings = Settings()
