# Import Libraries
from Config import APP_Settings
from Database import SessionLocal, DB_Engine
import Models
from kafka import KafkaConsumer
import json

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Define Consumer
Kafka_Consumer = KafkaConsumer(APP_Settings.KAFKA_TOPIC_RAW, 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    group_id="Data_Consumer", 
    auto_offset_reset='earliest',
    enable_auto_commit=False)

def Record_Message():

    try:

        for Message in Kafka_Consumer:

            # handle Message.
            Kafka_Message = json.loads(Message.value.decode())

            # Get Headers
            Command = Message.headers[0][1].decode('ASCII')
            Device_ID = Message.headers[1][1].decode('ASCII')
            Device_IP = Message.headers[2][1].decode('ASCII')

            # Print LOG
            print("Command     : ", Command)
            print("Device ID   : ", Device_ID)
            print("Client IP   : ", Device_IP)
            print(".........................................................")
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print(".........................................................")

            # Create Add Record Command
            New_Buffer_Post = Models.Incoming_Buffer(
                Buffer_Device_ID = Device_ID, 
                Buffer_Client_IP = Device_IP, 
                Buffer_Command = Command, 
                Buffer_Data = str(Kafka_Message))

            # Add and Refresh DataBase
            #db = Create_Database()
            db = SessionLocal()
            db.add(New_Buffer_Post)
            db.commit()
            db.refresh(New_Buffer_Post)

            # Close Database
            db.close()

            # Print LOG
            print("Message recorded to Buffer DB with Buffer_ID : ", New_Buffer_Post.Buffer_ID)
            print("---------------------------------------------------------")
            print("")

            # Commit Message
            Kafka_Consumer.commit()
            
    finally:
        print("Error Accured !!")

# Handle All Message in Topic
Record_Message()

