# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from datetime import datetime
from Functions import Kafka, Log, Handler

# Log Message
Log.Terminal_Log("INFO", f"***********************************************************************************")

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

    # Parse Topics
    for RAW_Message in Kafka.WeatherStat_Consumer:

        # Handle Headers
        RAW_Headers = Kafka.Handler_Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII')
        )

        # Log Message
        Log.Terminal_Log("INFO", f"New WeatherStat Received: {RAW_Headers.Device_ID}")

        # Decode Message
        Message = Kafka.Decode_WeatherStat_Message(RAW_Message)

        # Control for Latitude
        if Message.Latitude is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Latitude", Message.Latitude)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: Latitude - {Message.Latitude}")
        
        # Control for Longitude
        if Message.Longitude is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Longitude", Message.Longitude)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: Longitude - {Message.Longitude}")
        
        # Control for AT
        if Message.AT is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT", Message.AT)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AT - {Message.AT}")
        
        # Control for AH
        if Message.AH is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AH", Message.AH)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AH - {Message.AH}")
        
        # Control for AP
        if Message.AP is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AP", Message.AP)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AP - {Message.AP}")
        
        # Control for VL
        if Message.VL is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VL", Message.VL)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: VL - {Message.VL}")

        # Control for IR
        if Message.IR is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IR", Message.IR)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: IR - {Message.IR}")

        # Control for UV
        if Message.UV is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "UV", Message.UV)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: UV - {Message.UV}")

        # Control for R
        if Message.R is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "R", Message.R)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: R - {Message.R}")
        
        # Control for WD
        if Message.WD is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WD", Message.WD)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: WD - {Message.WD}")
        
        # Control for WS
        if Message.WS is not None: 
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WS", Message.WS)
            Log.Terminal_Log("INFO", f"New WeatherStat Received: WS - {Message.WS}")

        # Control for ST
        if Message.ST is not None:

            # Loop Through Measurements
            for index, ST_Value in enumerate(Message.ST):

                # Set Dynamic Variable Name
                ST_Variable_Name = f"ST{index}"

                # Add Measurement Record
                Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, ST_Variable_Name, ST_Value)
                Log.Terminal_Log("INFO", f"New WeatherStat Received: {ST_Variable_Name} - {ST_Value}")

        # Commit Kafka Consumer
        Kafka.WeatherStat_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Log Message
    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

    # Close Database
    DB_Module.close()
