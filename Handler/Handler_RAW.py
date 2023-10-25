# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka
from datetime import datetime
from Setup import Functions as Functions

# Parse Topics
def Parse_Topics():

    # Try to Parse Topics
    try:

        # Define DB
        DB_Module = Database.SessionLocal()

        # Parse Topics
        for RAW_Message in Kafka.Kafka_RAW_Consumer:

            # Get Headers
            RAW_Headers = Functions.Handle_Headers(RAW_Message)

            # Log Message
            Log.Terminal_Log("INFO", f"New Message Received")

            # Decode Message
            Kafka_RAW_Message = Kafka.Decode_RAW_Message(RAW_Message)

            # Control for Decoded Message
            if Kafka_RAW_Message is None:
                continue

            # Record DataStream
            try:

                # Create New DataStream
                New_Data_Stream = Models.Data_Stream(
                    Device_ID=RAW_Headers.Device_ID,
                    Data_Stream_Create_Date=datetime.now()
                )

                # Add Record to DataBase
                DB_Module.add(New_Data_Stream)

                # Commit DataBase
                DB_Module.commit()

                # Get DataStream ID
                Data_Stream_ID = str(New_Data_Stream.Data_Stream_ID)
                
            except Exception as e:
                
                # Log Message
                print(f"An error occurred while adding DataStream: {e}")

            # Control for DataStream ID
            if Data_Stream_ID is None:
                continue
            
            # Commit Kafka Consumer
            Kafka.Kafka_RAW_Consumer.commit()

            # Set Headers
            New_Headers = Functions.Parse_Headers(RAW_Headers, Data_Stream_ID)

            # Set Topics and Values
            Topics_And_Values = [
                
                # Device Info
                ("Device.Info", Kafka_RAW_Message.Device.Info.dict()),
                
                # Device Power
                ("Device.Power", Kafka_RAW_Message.Device.Power.dict()),
                
                # Device IoT
                ("Device.IoT", Kafka_RAW_Message.Device.IoT.dict()),

                # Device Payload
                ("Device.WeatherStat", Kafka_RAW_Message.Payload.WeatherStat.dict())

            ]

            # Send to Topic
            for Topic, Value in Topics_And_Values:
                
                # Send to Topic
                Kafka.Send_To_Topic(Topic, Value, New_Headers)

            # Log Message
            Log.Terminal_Log("INFO", f"-----------------------------------------------------------")

            # Log to Queue
            Kafka.Send_To_Log_Topic(RAW_Headers.Device_ID, f"RAW Data Parsed : {RAW_Headers.Device_IP}")

            # Commit Queue
            Kafka.Kafka_RAW_Consumer.commit()

    finally:

        # Log Message
        Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

        # Close Database
        DB_Module.close()

# Handle Device
Parse_Topics()
