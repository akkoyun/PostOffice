# Import Libraries
from Config import APP_Settings
from Database import SessionLocal, DB_Engine
import Models, Schema
from kafka import KafkaConsumer
import json
from json import dumps

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Define Consumer
Kafka_Consumer = KafkaConsumer('Device.IoT', 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    group_id="Data_Parser", 
    auto_offset_reset='earliest',
    enable_auto_commit=False)

def Info_Parser():

    try:

        for Message in Kafka_Consumer:

            # handle Message.
            Kafka_Message = json.loads(Message.value.decode())

            # Print LOG
            print("Command     : ", Message.headers[0][1].decode('ASCII'))
            print("Device ID   : ", Message.headers[1][1].decode('ASCII'))
            print("Client IP   : ", Message.headers[2][1].decode('ASCII'))
            print(".........................................................")
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print(".........................................................")
            print(Kafka_Message)
            print(".........................................................")
            print("")

            # Commit Message
            Kafka_Consumer.commit()

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Info_Parser()

