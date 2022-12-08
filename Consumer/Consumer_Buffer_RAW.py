# Import Libraries
from Config import APP_Settings
from Database import SessionLocal
from Models import Incoming_Buffer
from kafka import KafkaConsumer
from kafka import TopicPartition , OffsetAndMetadata
import json

# Define Consumer
Kafka_Consumer = KafkaConsumer(APP_Settings.KAFKA_TOPIC_RAW, 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id="Data_Consumer", 
    auto_offset_reset='earliest',
    enable_auto_commit=False)


def Record_Message():

    for Message in Kafka_Consumer:

        # handle Message
        Kafka_Message = json.loads(Message.value())

        # Get Headers
        Command = Message.headers[0][1].decode('ASCII')
        Device_ID = Message.headers[1][1].decode('ASCII')
        Device_IP = Message.headers[2][1].decode('ASCII')

        # Get Kafka Parameters
        Kafka_Key = Message.key
        Kafka_Topic = Message.topic
        Kafka_Partition = Message.partition
        Kafka_Offset = Message.offset
        Kafka_TimeStamp = Message.timestamp

        # Print LOG
        print("Command     : ", Command)
        print("Device ID   : ", Device_ID)
        print("Client IP   : ", Device_IP)
        print(".........................................................")
        print("Kafka Key : ", Kafka_Key, " - Topic : ", Kafka_Topic, " - Partition : ", Kafka_Partition, " - Offset : ", Kafka_Offset, " - TimeStamp : ", Kafka_TimeStamp)
        print(".........................................................")

        # Create Add Record Command
        New_Buffer_Post = Incoming_Buffer(Buffer_Device_ID = Device_ID, Buffer_Client_IP = Device_IP, Buffer_Command = Command, Buffer_Data = str(Kafka_Message))

        # Add and Refresh DataBase
        db = SessionLocal()
        db.add(New_Buffer_Post)
        db.commit()
        db.refresh(New_Buffer_Post)

        # Print LOG
        print("Message recorded to Buffer DB with Buffer_ID : ", New_Buffer_Post.Buffer_ID)
        print("---------------------------------------------------------")

        # Close Database
        db.close()

        # Commit Message
        TP = TopicPartition(Kafka_Topic, Kafka_Partition)
        OM = OffsetAndMetadata(Kafka_Offset + 1, Kafka_TimeStamp)
        Kafka_Consumer.commit({TP, OM})

# Handle All Message in Topic
Record_Message()

