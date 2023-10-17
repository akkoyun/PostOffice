# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="RAW_Consumer",
                               auto_offset_reset='latest',
                               enable_auto_commit=True)

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

# Kafka Callbacks
def Kafka_Send_Success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

# Kafka Callbacks
def Kafka_Send_Error(excp):
    print(f"Error: {excp}")

# Parse Topics
def Parse_Topics():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Try to Parse Topics
    try:

        # Parse Topics
        for RAW_Message in Kafka_Consumer:

            # Get Headers
            # -----------

            # Check if all required headers are present
            if len(RAW_Message.headers) >= 5:

                # Handle Headers
                class Headers:
                    Command = RAW_Message.headers[0][1].decode('ASCII')
                    Device_ID = RAW_Message.headers[1][1].decode('ASCII')
                    Device_Time = RAW_Message.headers[2][1].decode('ASCII')
                    Device_IP = RAW_Message.headers[3][1].decode('ASCII')
                    Size = RAW_Message.headers[4][1].decode('ASCII')

            # If not, log the error and skip to the next iteration
            else:
                
                # Log Message
                print(f"Header Error")
                
                # Skip to the next iteration
                continue

            # Decode Message
            # --------------

            # Decode Message
            Decoded_Value = RAW_Message.value.decode()

            # Parse JSON
            Parsed_JSON = json.loads(Decoded_Value)

            # Check if JSON is a string
            if isinstance(Parsed_JSON, str):
                Parsed_JSON = json.loads(Parsed_JSON)

            # Get RAW Data
            Kafka_RAW_Message = Schema.Data_Pack_Model(**Parsed_JSON)

            # Data Stream Record Add
            # ----------------------

            # Create New Data Stream Record
            New_Data_Stream = Models.Data_Stream(
                Device_ID = Headers.Device_ID
            )

            # Add Record to DataBase
            DB_Module.add(New_Data_Stream)

            # Commit DataBase
            DB_Module.commit()

            # Get New Data Stream ID
            Data_Stream_ID = New_Data_Stream.Data_Stream_ID

            # Set Headers
            # -----------

            # Set headers
            Kafka_Header = [
                ('Command', bytes(Headers.Command, 'utf-8')), 
                ('Device_ID', bytes(Headers.Device_ID, 'utf-8')),
                ('Device_Time', bytes(Headers.Device_Time, 'utf-8')), 
                ('Device_IP', bytes(Headers.Device_IP, 'utf-8')),
                ('Size', bytes(Headers.Size, 'utf-8')),
                ('Data_Stream_ID', bytes(Data_Stream_ID, 'utf-8'))
            ]

            # Send Message to Queue
            # ---------------------

			# Send Message to Queue
            Kafka_Producer.send("Device.Info", value=Kafka_RAW_Message.Device.Info.dict(), headers=Kafka_Header).add_callback(Kafka_Send_Success).add_errback(Kafka_Send_Error)
            Kafka_Producer.send("Device.Power", value=Kafka_RAW_Message.Device.Power.dict(), headers=Kafka_Header).add_callback(Kafka_Send_Success).add_errback(Kafka_Send_Error)
            Kafka_Producer.send("Device.IoT", value=Kafka_RAW_Message.Device.IoT.dict(), headers=Kafka_Header).add_callback(Kafka_Send_Success).add_errback(Kafka_Send_Error)

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Parse_Topics()
