# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Device_Consumer",
                               auto_offset_reset='earliest',
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

    # Try to Parse Topics
    try:

        # Parse Topics
        for RAW_Message in Kafka_Consumer:

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




            test_str = '{"key": "value"}'
            test_dict = json.loads(test_str)
            print(f"Decoded test dict: {test_dict}")
            print(f"Type of decoded test dict: {type(test_dict)}")





            # Set headers
            Kafka_Header = [
                ('Command', bytes(Headers.Command, 'utf-8')), 
                ('Device_ID', bytes(Headers.Device_ID, 'utf-8')),
                ('Device_Time', bytes(Headers.Device_Time, 'utf-8')), 
                ('Device_IP', bytes(Headers.Device_IP, 'utf-8')),
                ('Size', bytes(Headers.Size, 'utf-8'))
            ]

			# Send Message to Queue
#            Kafka_Producer.send("Device", value=Kafka_RAW_Message.Device.dict(), headers=Kafka_Header).add_callback(Kafka_Send_Success).add_errback(Kafka_Send_Error)

    finally:

        # Log Message
        print(f"Header Error")

# Handle Device
Parse_Topics()
