# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka
from datetime import datetime
from Setup import Functions as Functions

# Parse Topics
def Parse_Topics():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Try to Parse Topics
    try:

        # Parse Topics
        for RAW_Message in Kafka.Kafka_RAW_Consumer:

            # Log Message
            Log.Terminal_Log("INFO", f"New Message Received")

            # Get Headers
            RAW_Headers = Functions.Handle_Headers(RAW_Message)

            # Decode Message
            Kafka_RAW_Message = Kafka.Decode_RAW_Message(RAW_Message)

            # Control for Decoded Message
            if Kafka_RAW_Message is None:
                continue

            # Add DataStream Record
            Data_Stream_ID = str(Functions.DB_Datastream_Add_Record(RAW_Headers, DB_Module, Models))

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
                ("Device.IoT", Kafka_RAW_Message.Device.IoT.dict())

            ]

            # Send to Topic
            for Topic, Value in Topics_And_Values:
                
                # Send to Topic
                Kafka.Send_To_Topic(Topic, Value, New_Headers)

    finally:

    	# Log Message
	    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

# Handle Device
Parse_Topics()
