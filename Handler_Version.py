# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json
from datetime import datetime

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Device_Consumer",
                               auto_offset_reset='earliest',
                               enable_auto_commit=False)

# Parser Function
def Version_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:
        for Message in Kafka_Consumer:

            message_value = Message.value.decode('utf-8')
            print(f"Raw message_value: {message_value}")
            message_dict = json.loads(message_value)
            print(message_dict.get('Device', {}).get('Info', {}).get('Firmware', 'Firmware not found'))

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Version_Handler()
