# Import Libraries
from pydantic import BaseSettings
from kafka import KafkaConsumer, KafkaProducer
from json import dumps

# Define Setting
class Settings(BaseSettings):

	POSTOFFICE_DB_HOSTNAME: str
	POSTOFFICE_DB_PORT: str
	POSTOFFICE_DB_PASSWORD: str
	POSTOFFICE_DB_NAME: str
	POSTOFFICE_DB_USERNAME: str

	class Config:
		env_file = ".env"

# Set Setting
APP_Settings = Settings()

# Defne Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: dumps(m).encode('utf-8'), bootstrap_servers="165.227.154.147:9092")

# Define Kafka Consumer
Kafka_RAW_Consumer = KafkaConsumer('RAW', bootstrap_servers="165.227.154.147:9092", group_id="Data_Consumer", auto_offset_reset='earliest', enable_auto_commit=False)
Kafka_Info_Consumer = KafkaConsumer('Device.Info', bootstrap_servers="165.227.154.147:9092", group_id="Data_Parser", auto_offset_reset='earliest', enable_auto_commit=False)
Kafka_Power_Consumer = KafkaConsumer('Device.Power', bootstrap_servers="165.227.154.147:9092", group_id="Data_Parser", auto_offset_reset='earliest', enable_auto_commit=False)
Kafka_IoT_Consumer = KafkaConsumer('Device.IoT', bootstrap_servers="165.227.154.147:9092", group_id="Data_Parser", auto_offset_reset='earliest', enable_auto_commit=False)
Kafka_Payload_Consumer = KafkaConsumer('Device.Payload', bootstrap_servers="165.227.154.147:9092", group_id="Data_Parser", auto_offset_reset='earliest', enable_auto_commit=False)
