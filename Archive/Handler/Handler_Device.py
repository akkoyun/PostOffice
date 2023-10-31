# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Functions import Log
from datetime import datetime
from Functions import Functions as Functions, Kafka

# Parser Function
def Device_Handler():

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka.Kafka_Device_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Log Message
            Log.Terminal_Log("INFO", f"New Device Message Received : {Headers.Device_ID}")

            # Decode Message
            Kafka_Device_Message = Kafka.Decode_Device_Message(Message)

            # Device Update
            Functions.Device_Update(Headers, Kafka_Device_Message)

            # Version Update
            Functions.Version_Update(Headers, Kafka_Device_Message)

            # Power Update
            Functions.Power_Update(Headers, Kafka_Device_Message)

            # SIM Update
            Functions.SIM_Update(Headers, Kafka_Device_Message)

            # Module Update
            Functions.Module_Update(Headers, Kafka_Device_Message)




            # Connection Update
            Functions.Connection_Update(Headers, Kafka_Device_Message)

            # Location Update
            Functions.Location_Update(Headers, Kafka_Device_Message)

            # Log Message
            Log.Terminal_Log("INFO", f"-----------------------------------------------------------")

            # Commit Queue
            Kafka.Kafka_Device_Consumer.commit()

    finally:

        # Log Message
        Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

# Handle Device
Device_Handler()
