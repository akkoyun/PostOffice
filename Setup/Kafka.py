# Library Includes
from Setup.Config import APP_Settings
from Setup import Schema, Log
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
import time

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

# Kafka RAW Consumer
Kafka_RAW_Consumer = KafkaConsumer('RAW', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="RAW_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Power Consumer
Kafka_Power_Consumer = KafkaConsumer('Device.Power', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Power_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Info Consumer
Kafka_Info_Consumer = KafkaConsumer('Device.Info', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Device_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka IoT Consumer
Kafka_IoT_Consumer = KafkaConsumer('Device.IoT', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="IoT_Consumer", auto_offset_reset='latest', enable_auto_commit=False)



# Kafka Device Consumer
Kafka_Device_Consumer = KafkaConsumer('Pack.Device', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Device_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka WeatherStat Consumer
Kafka_WeatherStat_Consumer = KafkaConsumer('Device.WeatherStat', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="WeatherStat_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

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
        Kafka_Message = Schema.Data_Pack_Model(**Parsed_JSON)

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

# Decode and Parse Power Message
def Decode_Power_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Pack_Power(**Parsed_JSON)

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

# Decode and Parse Info Message
def Decode_Info_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Pack_Info(**Parsed_JSON)

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

# Decode and Parse Info Message
def Decode_IoT_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Pack_IoT(**Parsed_JSON)

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

# Decode and Parse Payload Message
def Decode_WeatherStat_Payload_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Payload_WeatherStat(**Parsed_JSON)

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



# Decode and Parse Device Message
def Decode_Device_Message(RAW_Message):
    
    try:

        # Decode Message
        Decoded_Value = RAW_Message.value.decode()
        
        # Parse JSON
        Parsed_JSON = json.loads(Decoded_Value)

        # Check if JSON is a string
        if isinstance(Parsed_JSON, str):
            Parsed_JSON = json.loads(Parsed_JSON)
        
        # Get RAW Data
        Kafka_Message = Schema.Pack_Device(**Parsed_JSON)

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



# Kafka Callbacks
def Send_Success(record_metadata):

	# Log Message
	Log.Terminal_Log("INFO", f"Send to Kafka Queue: {record_metadata.topic} / {record_metadata.partition} / {record_metadata.offset}")

# Kafka Callbacks
def Send_Error(excp):

	# Log Message
	Log.Terminal_Log("ERROR", f"Kafka Send Error: {excp}")

# Send to Topic
def Send_To_Topic(topic, value, headers, max_retries=3, delay=5):

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

# Send to Log Topic
def Send_To_Log_Topic(Device_ID, Message):

    # Set Message
    Message = {
        "Device_ID": Device_ID,
        "Message": Message,
        "TimeStamp": str(datetime.now())
    }

    # Send Message to Queue
    Kafka_Producer.send("LOG", value=Message)

    # Break Loop
    return
