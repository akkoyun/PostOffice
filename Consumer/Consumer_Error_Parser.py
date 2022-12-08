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
Kafka_Consumer = KafkaConsumer('Error', 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    group_id="Data_Parser", 
    auto_offset_reset='earliest',
    enable_auto_commit=False)

def Info_Parser():

    try:

        for Message in Kafka_Consumer:

            # handle Message.
            #Kafka_Message = json.loads(Message.value.decode())

            # Print LOG
            print(".........................................................")
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print(".........................................................")
            print(Message.value.decode())
            print(".........................................................")
            print("")

            # Commit Message
            Kafka_Consumer.commit()

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Info_Parser()

