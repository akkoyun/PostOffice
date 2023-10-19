# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
from Setup import Functions as Functions

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="RAW_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}')

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

        # Log Message
        Log.LOG_Message(f"New DataStream Record Added: {New_Data_Stream_ID}")

        # Return DataStream ID
        return New_Data_Stream_ID
    
    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding DataStream: {e}")

        # Return None
        return None

# Parse Topics
def Parse_Topics():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Try to Parse Topics
    try:

        # Parse Topics
        for RAW_Message in Kafka_Consumer:

            # Log Message
            Log.LOG_Message(f"Message Received")

            # Get Headers
            Headers = Functions.Handle_Headers(RAW_Message)

            # Decode Message
            Kafka_RAW_Message = Functions.Decode_Message(RAW_Message, Kafka_Consumer, Schema)

            # Control for Decoded Message
            if Kafka_RAW_Message is None:
                continue

            # Add DataStream Record
            Data_Stream_ID = str(DB_Datastream_Add_Record(Headers, DB_Module, Models))

            # Control for DataStream ID
            if Data_Stream_ID is None:
                continue
            
            # Commit Kafka Consumer
            Kafka_Consumer.commit()

            # Set Headers
            New_Headers = Functions.Parse_Headers(Headers, Data_Stream_ID)

            # Set Topics and Values
            Topics_And_Values = [
                
                # Device Info
                ("Device.Info", Kafka_RAW_Message.Device.Info.dict()),
                
                # Device Power
                ("Device.Power", Kafka_RAW_Message.Device.Power.dict()),
                
                # Device IoT
                ("Device.IoT", Kafka_RAW_Message.Device.IoT.dict())

            ]

            # Send to Topic
            for topic, value in Topics_And_Values:
                
                # Send to Topic
                Functions.Kafka_Send_To_Topic(topic, value, New_Headers)

    finally:

    	# Log Message
	    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

# Handle Device
Parse_Topics()
