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

class Headers:

    def __init__(self, headers):
        self.Command = headers[0][1].decode('ASCII')
        self.Device_ID = headers[1][1].decode('ASCII')
        self.Device_Time = headers[2][1].decode('ASCII')
        self.Device_IP = headers[3][1].decode('ASCII')
        self.Size = headers[4][1].decode('ASCII')


# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    try:
        for Message in Kafka_Consumer:

            print(Headers(Message.headers))


    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
