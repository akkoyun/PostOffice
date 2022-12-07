# Import Libraries
from Config import APP_Settings
from Database import SessionLocal
from Models import Incoming_Buffer
from kafka import KafkaConsumer
import json

# Define Consumer
Kafka_Consumer = KafkaConsumer(APP_Settings.KAFKA_TOPIC_RAW, 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    group_id="Data_Consumer", 
    enable_auto_commit=True)

def Record_Message():

    for Message in Kafka_Consumer:

        # Get Headers
        Command = Message.headers[0][1].decode('ASCII')
        Device_ID = Message.headers[1][1].decode('ASCII')
        Device_IP = Message.headers[2][1].decode('ASCII')

        # handle Message
        Kafka_Message = json.loads(Message.value.decode())

        print("Command     : ", Command)
        print("Device ID   : ", Device_ID)
        print("Client IP   : ", Device_IP)
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

# Handle All Message in Topic
Record_Message()
