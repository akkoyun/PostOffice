# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database
from Setup.Config import WeatherStat_Limits as Limits
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

        # Control for AT
        if Message.AT is not None and Message.AT >= Limits.AT_MIN and Message.AT <= Limits.AT_MAX:

            # Set AT
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT", Message.AT)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AT - {Message.AT}")

        # Control for AH
        if Message.AH is not None and Message.AH >= Limits.AH_MIN and Message.AH <= Limits.AH_MAX:

            # Set AH
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AH", Message.AH)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AH - {Message.AH}")

        # Control for AT_FL
        if Message.AT is not None and Message.AT >= Limits.AT_MIN and Message.AT <= Limits.AT_MAX and Message.AH is not None and Message.AH >= Limits.AH_MIN and Message.AH <= Limits.AH_MAX:

            # Calculate AT_FL
            AT_FL = Handler.FL_Calculator(Message.AT, Message.AH)

            # Calculate AT_Dew
            AT_Dew = Handler.Dew_Calculator(Message.AT, Message.AH)

            # Set AT_FL
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT_FL", AT_FL)

            # Set AT_Dew
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT_Dew", AT_Dew)
            
            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AT_FL - {AT_FL}")
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AT_Dew - {AT_Dew}")

        # Control for AP
        if Message.AP is not None and Message.AP >= Limits.AP_MIN and Message.AP <= Limits.AP_MAX:

            # Set AP
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AP", Message.AP)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: AP - {Message.AP}")

        # Control for VL
        if Message.VL is not None and Message.VL >= Limits.VL_MIN and Message.VL <= Limits.VL_MAX:

            # Set VL
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VL", Message.VL)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: VL - {Message.VL}")

        # Control for IR
        if Message.IR is not None and Message.IR >= Limits.IR_MIN and Message.IR <= Limits.IR_MAX:

            # Set IR
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IR", Message.IR)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: IR - {Message.IR}")

        # Control for UV
        if Message.UV is not None and Message.UV >= Limits.UV_MIN and Message.UV <= Limits.UV_MAX:

            # Set UV
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "UV", Message.UV)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: UV - {Message.UV}")

        # Control for R
        if Message.R is not None and Message.R >= Limits.R_MIN and Message.R <= Limits.R_MAX:

            # Calculate R
            R = Message.R / 200 # 1 tip is 5 ml

            # Set R
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "R", R)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: R - {R}")

        # Control for WD
        if Message.WD is not None and Message.WD >= Limits.WD_MIN and Message.WD <= Limits.WD_MAX:

            # Set WD
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WD", Message.WD)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: WD - {Message.WD}")
        
        # Control for WS
        if Message.WS is not None and Message.WS >= Limits.WS_MIN and Message.WS <= Limits.WS_MAX:

            # Set WS
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WS", Message.WS)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: WS - {Message.WS}")

        # Control for ST
        if Message.ST is not None:

            # Loop Through Measurements
            for index, ST_Value in enumerate(Message.ST):

                # Set Dynamic Variable Name
                ST_Variable_Name = f"ST{index}"

                # Get Variable Value
                ST_Value = ST_Value

                # Control for ST
                if ST_Value >= Limits.ST_MIN and ST_Value <= Limits.ST_MAX:

                    # Set ST
                    Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, ST_Variable_Name, ST_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New WeatherStat Received: {ST_Variable_Name} - {ST_Value}")

        # Control for Latitude
        if Message.Latitude is not None and Message.Latitude >= Limits.LATITUDE_MIN and Message.Latitude <= Limits.LATITUDE_MAX:

            # Set Latitude
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Latitude", Message.Latitude)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: Latitude - {Message.Latitude}")

        # Control for Longitude
        if Message.Longitude is not None and Message.Longitude >= Limits.LONGITUDE_MIN and Message.Longitude <= Limits.LONGITUDE_MAX:

            # Set Longitude
            Handler.WeatherStat_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Longitude", Message.Longitude)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Received: Longitude - {Message.Longitude}")

        # Commit Kafka Consumer
        Kafka.WeatherStat_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Log Message
    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

    # Close Database
    DB_Module.close()
