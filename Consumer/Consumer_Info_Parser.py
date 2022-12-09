# Import Libraries
from Setup.Config import Kafka_Info_Consumer
from Database import SessionLocal, DB_Engine
import Models, Schema
import json

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Info Parser Function
def Info_Parser():

    try:

        for Message in Kafka_Info_Consumer:

            # handle Message.
            Kafka_Info_Message = Schema.Pack_Info(**json.loads(Message.value.decode()))

            # Handle Headers
            Command = Message.headers[0][1].decode('ASCII')
            Device_ID = Message.headers[1][1].decode('ASCII')
            Device_Time = Message.headers[2][1].decode('ASCII')
            Device_IP = Message.headers[3][1].decode('ASCII')

            # Print LOG
            print("Command     : ", Command)
            print("Device ID   : ", Device_ID)
            print("Client IP   : ", Device_IP)
            print("Device Time : ", Device_Time)
            print(".........................................................")
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print(".........................................................")
            print(Kafka_Info_Message)

            # Create Add Record Command
            New_Info_Post = Models.Device_Info(
                Device_Time = Device_Time, 
                Device_ID = Device_ID, 
                Hardware_Version = Kafka_Info_Message.Hardware,
                Firmware_Version = Kafka_Info_Message.Firmware,
                Temperature = Kafka_Info_Message.Temperature,
                Humidity = Kafka_Info_Message.Humidity)

            # Add and Refresh DataBase
            db = SessionLocal()
            db.add(New_Info_Post)
            db.commit()
            db.refresh(New_Info_Post)

            # Print LOG
            print("Message recorded to Info DB with Info_ID : ", New_Info_Post.Info_ID)
            print(".........................................................")
            print("")
            # Close Database
            db.close()

            # Commit Message
            Kafka_Info_Consumer.commit()

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Info_Parser()

