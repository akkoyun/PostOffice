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

        # Define Formatted Data
        # 0 - Unknown
        # 1 - Device
        # 2 - Power
        # 3 - GSM
        # 4 - Location
        # 5 - Environment
        # 6 - Water
        # 7 - Energy

        # Control for Device Parameters
        for Device_Parameter_Name, Device_Parameter_Path in Type_List(1):
            if eval(Device_Parameter_Path) is not None:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Device_Parameter_Name, eval(Device_Parameter_Path))
            else:
                pass

        # Control for Location Parameters
        for Location_Parameter_Name, Location_Parameter_Path in Type_List(4):
            if eval(Location_Parameter_Path) is not None:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Location_Parameter_Name, eval(Location_Parameter_Path))
            else:
                pass

        # Control for WeatherStat Payloads
        for WeatherStat_Payload_Name, WeatherStat_Payload_Path in Type_List(5):
            try:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, WeatherStat_Payload_Name, eval(WeatherStat_Payload_Path))
            except:
                pass

        # Control for Water Payloads
        for Water_Payload_Name, Water_Payload_Path in Type_List(6):
            if eval(Water_Payload_Path) is not None: 
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Water_Payload_Name, eval(Water_Payload_Path))
            else:
                pass
            
        # Control for PowerStat Payloads
        for PowerStat_Payload_Name, PowerStat_Payload_Path in Type_List(7):
            if eval(PowerStat_Payload_Path) is not None: 
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PowerStat_Payload_Name, eval(PowerStat_Payload_Path))
            else:
                pass

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
