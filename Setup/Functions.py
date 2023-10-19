# Library Includes
from kafka import KafkaConsumer, KafkaProducer
from Setup.Config import APP_Settings
from datetime import datetime
import Log
import json
import time

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

# Kafka Callbacks
def Kafka_Send_Success(record_metadata):

	# Log Message
	Log.LOG_Message(f"Send to Kafka Queue: {datetime.now()} - {record_metadata.topic} / {record_metadata.partition} / {record_metadata.offset}")

# Kafka Callbacks
def Kafka_Send_Error(excp):

	# Log Message
	Log.LOG_Error_Message(f"Kafka Send Error: {excp} - {datetime.now()}")

# Define Incomming Headers
class Incomming_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size

# Define Full Headers
class Full_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size, data_stream_id):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size
        self.Data_Stream_ID = data_stream_id

# Handle Incomming Headers
def Handle_Headers(message):

    # Check if all required headers are present    
    if len(message.headers) >= 5:
    
        # Handle Headers
        headers = Incomming_Headers(
            message.headers[0][1].decode('ASCII'),
            message.headers[1][1].decode('ASCII'),
            message.headers[2][1].decode('ASCII'),
            message.headers[3][1].decode('ASCII'),
            message.headers[4][1].decode('ASCII')
        )

        # Return Headers
        return headers
    
    else:

        # Log Message
        Log.Device_Header_Handler_Error()

        # Skip to the next iteration
        return None

# Handle Full Headers
def Handle_Full_Headers(message):

    # Check if all required headers are present    
    if len(message.headers) >= 6:
    
        # Handle Headers
        headers = Full_Headers(
            message.headers[0][1].decode('ASCII'),
            message.headers[1][1].decode('ASCII'),
            message.headers[2][1].decode('ASCII'),
            message.headers[3][1].decode('ASCII'),
            message.headers[4][1].decode('ASCII'),
            message.headers[5][1].decode('ASCII')
        )

        # Return Headers
        return headers
    
    else:

        # Log Message
        Log.Device_Header_Handler_Error()

        # Skip to the next iteration
        return None

# Parse Headers
def Parse_Headers(Headers, Data_Stream_ID):

    try:

        # Set headers
        Kafka_Header = [
            ('Command', bytes(Headers.Command, 'utf-8')), 
            ('Device_ID', bytes(Headers.Device_ID, 'utf-8')),
            ('Device_Time', bytes(Headers.Device_Time, 'utf-8')), 
            ('Device_IP', bytes(Headers.Device_IP, 'utf-8')),
            ('Size', bytes(Headers.Size, 'utf-8')),
            ('Data_Stream_ID', bytes(Data_Stream_ID, 'utf-8'))
        ]

        # Return Kafka Header
        return Kafka_Header

    except Exception as e:

        # Log Message
        print(f"An error occurred while setting Kafka headers: {e}")
        
        # Return None
        return None

# Decode and Parse Message
def Decode_Message(RAW_Message, Kafka_Consumer, Schema):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_RAW_Message = Schema.Data_Pack_Model(**Parsed_JSON)

        return Kafka_RAW_Message

    except json.JSONDecodeError:
        print("JSON Decode Error")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Decode and Parse Message IoT Hub
def Decode_IoT_Message(RAW_Message, Kafka_Consumer, Schema):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_RAW_Message = Schema.Pack_IoT(**Parsed_JSON)

        return Kafka_RAW_Message

    except json.JSONDecodeError:
        print("JSON Decode Error")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Add DataStream Record
def DB_Datastream_Add_Record(Headers, DB_Module, Models):

    try:

        # Create New DataStream
        New_Data_Stream = Models.Data_Stream(
            Device_ID=Headers.Device_ID,
            Data_Stream_Create_Date=datetime.now()
        )

        # Add Record to DataBase
        DB_Module.add(New_Data_Stream)

        # Commit DataBase
        DB_Module.commit()

        # Get DataStream ID
        New_Data_Stream_ID = str(New_Data_Stream.Data_Stream_ID)
        
        # Return DataStream ID
        return New_Data_Stream_ID
    
    except Exception as e:
        
        # Log Message
        print(f"An error occurred while adding DataStream: {e}")
        
        # Return None
        return None

# Send to Topic
def Kafka_Send_To_Topic(topic, value, headers, max_retries=3, delay=5):

    # Define Retry Counter
    Retries = 0

    # Try to Send Message
    while Retries < max_retries:

        try:

            # Send Message to Queue
            Kafka_Producer.send(topic, value=value, headers=headers).add_callback(Kafka_Send_Success).add_errback(Kafka_Send_Error)

            # Break Loop
            return

        except Exception as e:

            # Log Message
            print(f"Failed to send message to {topic}. Attempt {Retries+1} of {max_retries}. Error: {e}")

            # Increment Retry Counter
            Retries += 1

            # Sleep
            time.sleep(delay)

    # Log Message
    print(f"Failed to send message to {topic} after {max_retries} attempts.")
