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

        # Control for Device Parameters
        for Device_Parameter_Name, Device_Parameter_Path in Type_List(1):

            # Control Payload Path
            if Device_Parameter_Path is not None:

                try:

                    # Get Parameter Path
                    Non_Device_Message_Path = eval(Device_Parameter_Path)

                    # Handle Parameter
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Device_Parameter_Name, Non_Device_Message_Path)

                except Exception as e:

                    continue

        # Control for Location Parameters
        for Location_Parameter_Name, Location_Parameter_Path in Type_List(4):

            # Control Payload Path
            if Location_Parameter_Path is not None:

                try:

                    # Get Parameter Path
                    Non_Device_Message_Path = eval(Location_Parameter_Path)

                    # Handle Parameter
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Location_Parameter_Name, Non_Device_Message_Path)

                except Exception as e:

                    continue

        # Control for WeatherStat Payloads
        for WeatherStat_Payload_Name, WeatherStat_Payload_Path in Type_List(5):

            # Control Payload Path
            if WeatherStat_Payload_Path is not None:

                try:

                    # Get Parameter Path
                    WeatherStat_Message_Path = eval(WeatherStat_Payload_Path)

                    # Handle Parameter
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, WeatherStat_Payload_Name, WeatherStat_Message_Path)

                except Exception as e:

                    continue

        # Control for PowerStat Payloads
        for PowerStat_Payload_Name, PowerStat_Payload_Path in Type_List(7):

            # Control Payload Path
            if PowerStat_Payload_Path is not None:

                try:

                    # Get Parameter Path
                    PowerStat_Message_Path = eval(PowerStat_Payload_Path)

                    # Handle Parameter
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PowerStat_Payload_Name, PowerStat_Message_Path)

                except Exception as e:

                    continue

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
