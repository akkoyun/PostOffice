# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Definitions
from Functions import Kafka, Log, Handler
from Setup.Definitions import Type_List

# Try to Parse Topics
try:

    # Parse Topics
    for RAW_Message in Kafka.Parameter_Consumer:

        # Handle Headers
        RAW_Headers = Definitions.Handler_Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII')
        )

        # Convert Device Time (str) to datetime
        Device_Time = RAW_Headers.Device_Time.replace("T", " ").replace("Z", "")

        # Decode Message
        Message = Kafka.Decode_Device_Message(RAW_Message)

        # Define Formatted Data
        # 0 - Unknown
        # 1 - Device
        # 2 - Power
        # 3 - GSM
        # 4 - Location
        # 5 - Environment
        # 6 - Water
        # 7 - Energy

        # Control for Battery Parameters
        for Battery_Parameter_Name, Battery_Parameter_Path in Type_List(2):
            try:
                Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, Battery_Parameter_Name, eval(Battery_Parameter_Path))
            except:
                pass

        # Control for GSM Parameters
        for GSM_Parameter_Name, GSM_Parameter_Path in Type_List(3):
            try:
                Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, GSM_Parameter_Name, eval(GSM_Parameter_Path))
            except:
                pass

        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"******************************")

# Handle Errors
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Parameter Handler Error: {e}")
