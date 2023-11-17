# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Definitions
from Setup.Definitions import Type_List
from Functions import Kafka, Log, Handler

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

    # Parse Topics
    for RAW_Message in Kafka.Payload_Consumer:

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
        Message = Kafka.Decode_Payload_Message(RAW_Message)

        # Control for Non Device Parameters
        for Non_Device_Parameter_Name, Non_Device_Parameter_Path in Definitions.Type_List(0):
            if eval(Non_Device_Parameter_Path) is not None: Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Non_Device_Parameter_Name, eval(Non_Device_Parameter_Path))

        # Control for WeatherStat Payloads
        for WeatherStat_Parameter_Name, WeatherStat_Parameter_Path in Definitions.Type_List(4):
            if eval(WeatherStat_Parameter_Path) is not None: Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, WeatherStat_Parameter_Name, eval(WeatherStat_Parameter_Path))

        # Control for PowerStat Payloads
        for PowerStat_Parameter_Name, PowerStat_Parameter_Path in Definitions.Type_List(6):
            if eval(PowerStat_Parameter_Path) is not None: Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PowerStat_Parameter_Name, eval(PowerStat_Parameter_Path))

        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"******************************")

# Handle Errors
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Payload Handler Error: {e}")

# Close Database
finally:

    # Close Database
    DB_Module.close()
