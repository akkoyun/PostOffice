# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Definitions
from Setup.Definitions import Non_Device_Parameter, WeatherStat_Payload, PowerStat_Payload
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
        for Non_Device_Parameter_Name, Non_Device_Parameter_Path in Non_Device_Parameter:

            # Get Parameter Path
            Non_Device_Message_Path = eval(Non_Device_Parameter_Path)

            # Handle Parameter
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Non_Device_Parameter_Name, Non_Device_Message_Path)

        # Control for WeatherStat Payloads
        for WeatherStat_Payload_Name, WeatherStat_Payload_Path in WeatherStat_Payload:

            # Get Parameter Path
            WeatherStat_Message_Path = eval(WeatherStat_Payload_Path)

            # Handle Parameter
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, WeatherStat_Payload_Name, WeatherStat_Message_Path)

        # Control for PowerStat Payloads
        for PowerStat_Payload_Name, PowerStat_Payload_Path in PowerStat_Payload:

            # Get Parameter Path
            PowerStat_Message_Path = eval(PowerStat_Payload_Path)

            # Handle Parameter
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PowerStat_Payload_Name, PowerStat_Message_Path)

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
