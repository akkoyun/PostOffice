# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Definitions
from Setup.Definitions import Type_List
from Functions import Kafka, Log, Handler, Functions

# Try to Parse Topics
try:

    # Parse Topics
    for RAW_Message in Kafka.Payload_Consumer:

        # Handle Headers
        RAW_Headers = Definitions.Handler_Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII'),
            RAW_Message.headers[6][1].decode('ASCII'),
            RAW_Message.headers[7][1].decode('ASCII'),
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
            try:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Device_Parameter_Name, eval(Device_Parameter_Path))
            except:
                pass

        # Control for Location Parameters
        for Location_Parameter_Name, Location_Parameter_Path in Type_List(4):
            try:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Location_Parameter_Name, eval(Location_Parameter_Path))
            except:
                pass

        # Control for WeatherStat Payloads
#        for WeatherStat_Payload_Name, WeatherStat_Payload_Path in Type_List(5):
#            try:
#                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, WeatherStat_Payload_Name, eval(WeatherStat_Payload_Path))
#            except:
#                pass

        # Control for Water Payloads
        for Water_Payload_Name, Water_Payload_Path in Type_List(6):
            try:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Water_Payload_Name, eval(Water_Payload_Path))
            except: 
                pass

        # Control for PowerStat Payloads
        for PowerStat_Payload_Name, PowerStat_Payload_Path in Type_List(7):
            try:
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PowerStat_Payload_Name, eval(PowerStat_Payload_Path))
            except:
                pass













        for Type_ID, Variable, Description, Unit, Segment_ID in Definitions.Variable_List(5):

            # Set Data Pack
            Measurement = Definitions.Measurement_Class(
                type_id=Type_ID, 
                variable=Variable, 
                path=f"Message.{Variable.Variable}",
                value=eval(f"Message.{Variable.Variable}"),
                description=Description, 
                unit=Unit, 
                segment_id=Segment_ID,
                stream_id=RAW_Headers.Stream_ID,
                device_time=Device_Time
            )

            Log.Terminal_Log("INFO", f"Measurement: {Measurement}")

            # Record Payload
#            Functions.Measurement_Recorder(Measurement)













        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"******************************")

# Handle Errors
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Payload Handler Error: {e}")
