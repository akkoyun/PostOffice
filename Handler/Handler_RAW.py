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

            # Define DataStream ID
            Data_Stream_ID = 0

            # Record DataStream
            try:

                # Create New DataStream
                New_Data_Stream = Models.Stream(
                    Device_ID=RAW_Headers.Device_ID,
                    IMEI=Kafka_RAW_Message.Device.IoT.GSM.Module.IMEI,
                    ICCID=Kafka_RAW_Message.Device.IoT.GSM.Operator.ICCID,
                    RSSI=Kafka_RAW_Message.Device.IoT.GSM.Operator.RSSI,
                    Device_IP=RAW_Headers.Device_IP,
                    Connection_Time=Kafka_RAW_Message.Device.IoT.GSM.Operator.ConnTime,
                    Size=RAW_Headers.Size,
                    Create_Date=datetime.now()
                )

                # Add Record to DataBase
                DB_Module.add(New_Data_Stream)

                # Commit DataBase
                DB_Module.commit()

                # Get DataStream ID
                Data_Stream_ID = New_Data_Stream.Stream_ID

            except Exception as e:
                
                # Log Message
                print(f"An error occurred while adding DataStream: {e}")
    
            # Commit Kafka Consumer
            Kafka.Kafka_RAW_Consumer.commit()

            # Set Headers
            New_Headers = Functions.Parse_Headers(RAW_Headers, Data_Stream_ID)

            # Log Message
            Log.Terminal_Log("INFO", f"New Valid RAW Data Record Added: ['{Data_Stream_ID}' - '{RAW_Headers.Device_ID}' - '{RAW_Headers.Device_IP}']")

            # Set Topics and Values
            Topics_And_Values = [

                # Device Info
                ("Pack.Device", Kafka_RAW_Message.Device.dict()),

                # Device Payload
                ("Pack.WeatherStat", Kafka_RAW_Message.Payload.WeatherStat.dict())

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
