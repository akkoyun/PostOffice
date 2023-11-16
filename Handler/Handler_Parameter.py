# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Definitions
from Setup.Definitions import Parameter
from Functions import Kafka, Log, Handler

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

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

        # Control for Parameters
        for Parameter_Name, Parameter_Path in Parameter:

            # Get Parameter Path
            Message_Path = eval(Parameter_Path)

            # Handle Parameter
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, Parameter_Name, Message_Path)

        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

# Handle Errors
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Parameter Handler Error: {e}")

finally:

    # Close Database
    DB_Module.close()
