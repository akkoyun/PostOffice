# Import Libraries
from Config import APP_Settings
from Database import SessionLocal, DB_Engine
import Models, Schema
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import json
from json import dumps

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Define Consumer
Kafka_Consumer = KafkaConsumer(APP_Settings.KAFKA_TOPIC_RAW, 
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", 
    group_id="Data_Consumer", 
    auto_offset_reset='earliest',
    enable_auto_commit=False)

# Defne Kafka Producer
Kafka_Producer = KafkaProducer(
    value_serializer=lambda m: dumps(m).encode('utf-8'),
    bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}")

def Handle_RAW_Topic():

    try:

        for Message in Kafka_Consumer:

            # handle Message.
            Kafka_Message = Schema.IoT_Data_Pack_Model(**json.loads(Message.value.decode()))

            # Handle Headers
            Command = Message.headers[0][1].decode('ASCII')
            Device_ID = Message.headers[1][1].decode('ASCII')
            Device_IP = Message.headers[2][1].decode('ASCII')
            Device_Time = Kafka_Message.Payload.TimeStamp

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
            Kafka_Consumer.commit()



            # Set Header
            Kafka_Handle_Headers = [('ID', bytes(Device_ID, 'utf-8')), ('Device_Time', bytes(Device_Time, 'utf-8'))]

            # Send Info Message to Queue
            try:
                Kafka_Producer.send("Device.Info", value=Kafka_Message.Device.Info.dict(exclude={'ID'}), headers=Kafka_Handle_Headers)
            except KafkaError as exc:
                print("Exception (Info) during getting assigned partitions - {}".format(exc))
                pass

            # Send Power Message to Queue
            try:
                Kafka_Producer.send("Device.Power", value=Kafka_Message.Device.Power.dict(), headers=Kafka_Handle_Headers)
            except KafkaError as exc:
                print("Exception (Power) during getting assigned partitions - {}".format(exc))
                pass

            # Send IoT Message to Queue
            try:
                Kafka_Producer.send("Device.IoT", value=Kafka_Message.Device.IoT.dict(), headers=Kafka_Handle_Headers)
            except KafkaError as exc:
                print("Exception (IoT) during getting assigned partitions - {}".format(exc))
                pass

            # Send Payload Message to Queue
            try:
                Kafka_Producer.send("Device.Payload", value=Kafka_Message.Device.Payload.dict(exclude={'TimeStamp'}), headers=Kafka_Handle_Headers)
            except KafkaError as exc:
                print("Exception (Payload) during getting assigned partitions - {}".format(exc))
                pass


            print("Message parsed to consumers...")
            print("---------------------------------------------------------")

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Handle_RAW_Topic()

