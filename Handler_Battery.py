# Library Includes
import Setup.Functions as Functions
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('Device.Power', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="Power_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Power Measurement Handler Function
def Power_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka_Consumer:

            # Log Message
            Log.LOG_Message(f"Message Received")

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Decode Message
            try:

                # Decode Message
                Decoded_Value = Message.value.decode()
                
                # Parse JSON
                Parsed_JSON = json.loads(Decoded_Value)

                # Check if JSON is a string
                if isinstance(Parsed_JSON, str):
                    Parsed_JSON = json.loads(Parsed_JSON)
                
                # Get RAW Data
                Kafka_Power_Message = Schema.Pack_Power(**Parsed_JSON)

            except json.JSONDecodeError:

                # Log Message
                Log.LOG_Error_Message(f"JSON Decode Error")

            except Exception as e:

                # Log Message
                Log.LOG_Error_Message(f"An error occurred: {e}")

            # Add IV Measurement Record
            if Kafka_Power_Message.Battery.IV is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'IV', Kafka_Power_Message.Battery.IV)

            # Add AC Measurement Record
            if Kafka_Power_Message.Battery.AC is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'AC', Kafka_Power_Message.Battery.AC)

            # Add FB Measurement Record
            if Kafka_Power_Message.Battery.FB is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'FB', Kafka_Power_Message.Battery.FB)
            
            # Add IB Measurement Record
            if Kafka_Power_Message.Battery.IB is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'IB', Kafka_Power_Message.Battery.IB)
            
            # Add SOC Measurement Record
            if Kafka_Power_Message.Battery.SOC is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'SOC', Kafka_Power_Message.Battery.SOC)
            
            # Add T Measurement Record
            if Kafka_Power_Message.Battery.T is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'T', Kafka_Power_Message.Battery.T)

            # Add Charge Measurement Record
            if Kafka_Power_Message.Battery.Charge is not None:

                # Add Measurement Record
                Functions.Add_Measurement_Record(DB_Module, Models, Headers, Log, 'Charge', Kafka_Power_Message.Battery.Charge)

            # Commit Queue
            Kafka_Consumer.commit()

    finally:

        # Close Database
        DB_Module.close()            

# Handle Device
Power_Handler()
