# Library Includes
from Setup.Config import APP_Settings
from Setup import Schema, Log
from kafka import KafkaConsumer
import json

# Kafka Power Consumer
Kafka_Power_Consumer = KafkaConsumer('Device.Power', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Power_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Info Consumer
Kafka_Info_Consumer = KafkaConsumer('Device.Info', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Device_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Consumer
Kafka_IoT_Consumer = KafkaConsumer('Device.IoT', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="IoT_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

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
