# Import Libraries
from ..Setup.Config import Kafka_RAW_Consumer
from ..Setup.Config import KafkaProducer as Kafka_Producer
from Database import SessionLocal, DB_Engine
import Models, Schema
import json

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

def Handle_RAW_Topic():

    try:

        for Message in Kafka_RAW_Consumer:

            # handle Message.
            Kafka_Message = Schema.IoT_Data_Pack_Model(**json.loads(Message.value.decode()))

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

            # Create Add Record Command
            New_Buffer_Post = Models.Incoming_Buffer(
                Buffer_Device_ID = Device_ID, 
                Buffer_Client_IP = Device_IP, 
                Buffer_Command = Command, 
                Buffer_Data = str(Kafka_Message))

            # Add and Refresh DataBase
            db = SessionLocal()
            db.add(New_Buffer_Post)
            db.commit()
            db.refresh(New_Buffer_Post)

            # Print LOG
            print("Message recorded to Buffer DB with Buffer_ID : ", New_Buffer_Post.Buffer_ID)
            print(".........................................................")

            # Close Database
            db.close()

            # Commit Message
            Kafka_RAW_Consumer.commit()


            # Set headers
            Kafka_Parser_Headers = [
                ('Command', bytes(Command, 'utf-8')), 
                ('ID', bytes(Device_ID, 'utf-8')), 
                ('Device_Time', bytes(Device_Time, 'utf-8')), 
                ('IP', bytes(Device_IP, 'utf-8'))]

            # Send Parsed Message to Queue
            Kafka_Producer.send("Device.Info", value=Kafka_Message.Device.Info.dict(exclude={'ID'}), headers=Kafka_Parser_Headers)
            Kafka_Producer.send("Device.Power", value=Kafka_Message.Device.Power.dict(), headers=Kafka_Parser_Headers)
            Kafka_Producer.send("Device.IoT", value=Kafka_Message.Device.IoT.dict(), headers=Kafka_Parser_Headers)
            Kafka_Producer.send("Device.Payload", value=Kafka_Message.Payload.dict(exclude={'TimeStamp'}), headers=Kafka_Parser_Headers)

            print("Message parsed to consumers...")
            print("---------------------------------------------------------")

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Handle_RAW_Topic()

