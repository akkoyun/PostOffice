# Library Includes
from Functions import Log
from Setup.Config import APP_Settings
from Setup import Schema
from kafka import KafkaConsumer, KafkaProducer
import json
import time

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}')

# Kafka RAW Consumer
RAW_Consumer = KafkaConsumer(str(APP_Settings.KAFKA_TOPIC_RAW), bootstrap_servers=f"{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}", group_id=str(APP_Settings.KAFKA_CONSUMER_RAW_GROUP), auto_offset_reset='latest', enable_auto_commit=False)

# Define Headers
class Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size

# Kafka Callbacks
def Send_Success(record_metadata):

	# Log Message
	Log.Terminal_Log("INFO", f"Send to Kafka Queue: {record_metadata.topic} / {record_metadata.partition} / {record_metadata.offset}")

# Kafka Callbacks
def Send_Error(excp):

	# Log Message
	Log.Terminal_Log("ERROR", f"Kafka Send Error: {excp}")

# Send to Topic
def Send_To_Topic(topic: str, value, headers, max_retries=3, delay=5):

    # Define Retry Counter
    Retries = 0

    # Try to Send Message
    while Retries < max_retries:

        try:

            # Send Message to Queue
            Kafka_Producer.send(topic, value=value, headers=headers).add_callback(Send_Success).add_errback(Send_Error)

            # Break Loop
            return

        except Exception as e:

            # Log Message
            Log.Terminal_Log("INFO", f"Failed to send message to {topic}. Attempt {Retries+1} of {max_retries}. Error: {e}")

            # Increment Retry Counter
            Retries += 1

            # Sleep
            time.sleep(delay)

    # Log Message
    Log.Terminal_Log("INFO", f"Failed to send message to {topic} after {max_retries} attempts.")

# Parse Headers
def Parse_Topic_Header(Command, Device_ID, Device_Time, Device_IP, Pack_Size):

    try:

        # Set headers
        RAW_Header = [
            ('Command', bytes(Command, 'utf-8')), 
            ('Device_ID', bytes(Device_ID, 'utf-8')),
            ('Device_Time', bytes(Device_Time, 'utf-8')), 
            ('Device_IP', bytes(Device_IP, 'utf-8')),
            ('Size', bytes(Pack_Size, 'utf-8')),
        ]

        # Return Kafka Header
        return RAW_Header

    except Exception as e:

        # Log Message
        print(f"An error occurred while setting RAW topic headers: {e}")
        
        # Return None
        return None

# Handle Incomming Headers
def Handle_Headers(message):

    # Check if all required headers are present    
    if len(message.headers) >= 5:
    
        # Handle Headers
        headers = Headers(
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

# Decode and Parse Power Message
def Decode_RAW_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Data_Pack(**Parsed_JSON)

        # Return Kafka_Message
        return Kafka_Message

    except json.JSONDecodeError:
        
        # Log Message
        Log.Terminal_Log("ERROR", f"JSON Decode Error: {e}")

        # Return None
        return None
    
    except Exception as e:
    
        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred: {e}")

        # Return None
        return None
