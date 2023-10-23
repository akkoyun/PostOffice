# Library Includes
from Setup.Config import APP_Settings
from kafka import KafkaConsumer

# Kafka Power Consumer
Kafka_Power_Consumer = KafkaConsumer('Device.Power', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Power_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Info Consumer
Kafka_Info_Consumer = KafkaConsumer('Device.Info', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Device_Consumer", auto_offset_reset='latest', enable_auto_commit=False)
