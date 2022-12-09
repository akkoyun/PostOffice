from pydantic import BaseSettings
from kafka import KafkaConsumer

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

# Define Consumer
Kafka_Info_Consumer = KafkaConsumer('Device.Info', bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", group_id="Data_Parser", auto_offset_reset='earliest', enable_auto_commit=False)
