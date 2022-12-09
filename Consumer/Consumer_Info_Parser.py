# Import Libraries
from Config import Kafka_Info_Consumer
from Database import SessionLocal, DB_Engine
import Models, Schema
from kafka import KafkaConsumer
import json
from json import dumps

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Info Parser Function
def Info_Parser():

    try:

        for Message in Kafka_Info_Consumer:

            # handle Message.
            Kafka_Message = json.loads(Message.value.decode())

            # Print LOG
            print("Command : ", Message.headers[0][1].decode('ASCII'), " Device_ID : ", Message.headers[1][1].decode('ASCII'), " Client IP : ", Message.headers[2][1].decode('ASCII'))
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print(".....................................................................................................")
            print(Kafka_Message)
            print(".....................................................................................................")
            print("")

            # Commit Message
            Kafka_Info_Consumer.commit()

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Info_Parser()

