# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database
from Setup.Config import Payload_Limits as Limits
from datetime import datetime
from Functions import Kafka, Log, Handler

# Log Message
Log.Terminal_Log("INFO", f"***********************************************************************************")

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

    # Parse Topics
    for RAW_Message in Kafka.Payload_Consumer:

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
        Log.Terminal_Log("INFO", f"New Data Received: {RAW_Headers.Device_ID}")

        # Decode Message
        Message = Kafka.Decode_Payload_Message(RAW_Message)

        # Control for Latitude
        if Message.Latitude is not None and Message.Latitude > Limits.LATITUDE_MIN and Message.Latitude < Limits.LATITUDE_MAX:

            # Set Latitude
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Latitude", Message.Latitude)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> Latitude : {Message.Latitude}")

        # Control for Longitude
        if Message.Longitude is not None and Message.Longitude > Limits.LONGITUDE_MIN and Message.Longitude < Limits.LONGITUDE_MAX:

            # Set Longitude
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Longitude", Message.Longitude)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> Longitude : {Message.Longitude}")

        # WeatherStat Payloads

        # Control for AT
        if Message.AT is not None and Message.AT > Limits.AT_MIN and Message.AT < Limits.AT_MAX:

            # Set AT
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT", Message.AT)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> AT : {Message.AT}")

        # Control for AH
        if Message.AH is not None and Message.AH > Limits.AH_MIN and Message.AH < Limits.AH_MAX:

            # Set AH
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AH", Message.AH)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> AH : {Message.AH}")

        # Control for AT_FL
        if Message.AT is not None and Message.AT > Limits.AT_MIN and Message.AT < Limits.AT_MAX and Message.AH is not None and Message.AH > Limits.AH_MIN and Message.AH < Limits.AH_MAX:

            # Calculate AT_FL
            AT_FL = Handler.FL_Calculator(Message.AT, Message.AH)

            # Calculate AT_Dew
            AT_Dew = Handler.Dew_Calculator(Message.AT, Message.AH)

            # Control for AT_FL
            if AT_FL is not None and AT_FL >= Limits.AT_MIN and AT_FL <= Limits.AT_MAX:
                
                # Set AT_FL
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT_FL", AT_FL)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AT_FL : {AT_FL}")

            # Control for AT_Dew
            if AT_Dew is not None and AT_Dew >= Limits.AT_MIN and AT_Dew <= Limits.AT_MAX:

                # Set AT_Dew
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AT_Dew", AT_Dew)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AT_Dew : {AT_Dew}")

        # Control for AP
        if Message.AP is not None and Message.AP > Limits.AP_MIN and Message.AP < Limits.AP_MAX:

            # Set AP
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AP", Message.AP)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> AP : {Message.AP}")

        # Control for VL
        if Message.VL is not None and Message.VL > Limits.VL_MIN and Message.VL < Limits.VL_MAX:

            # Set VL
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VL", Message.VL)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> VL : {Message.VL}")

        # Control for IR
        if Message.IR is not None and Message.IR > Limits.IR_MIN and Message.IR < Limits.IR_MAX:

            # Set IR
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IR", Message.IR)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> IR : {Message.IR}")

        # Control for UV
        if Message.UV is not None and Message.UV > Limits.UV_MIN and Message.UV < Limits.UV_MAX:

            # Set UV
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "UV", Message.UV)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> UV : {Message.UV}")

        # Control for R
        if Message.R is not None and Message.R > Limits.R_MIN and Message.R < Limits.R_MAX:

            # Calculate R
            R = Message.R / 200 # 1 tip is 5 ml

            # Set R
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "R", R)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> R : {R}")

        # Control for WD
        if Message.WD is not None and Message.WD > Limits.WD_MIN and Message.WD < Limits.WD_MAX:

            # Set WD
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WD", Message.WD)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> WD : {Message.WD}")
        
        # Control for WS
        if Message.WS is not None and Message.WS > Limits.WS_MIN and Message.WS < Limits.WS_MAX:

            # Set WS
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "WS", Message.WS)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> WS : {Message.WS}")

        # Control for ST
        if Message.ST is not None:

            # Loop Through Measurements
            for index, ST_Value in enumerate(Message.ST):

                # Set Dynamic Variable Name
                ST_Variable_Name = f"ST{index}"

                # Get Variable Value
                ST_Value = ST_Value

                # Control for ST
                if ST_Value > Limits.ST_MIN and ST_Value < Limits.ST_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, ST_Variable_Name, ST_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {ST_Variable_Name} : {ST_Value}")

        # PowerStat Payloads

        # Control for Instant Voltage
        if Message.V is not None:

            # Loop Through Measurements
            for index, V_Value in enumerate(Message.V):

                # Set Dynamic Variable Name
                if index == 0: V_Variable_Name = f"V_R"
                if index == 1: V_Variable_Name = f"V_S"
                if index == 2: V_Variable_Name = f"V_T"
                if index == 3: V_Variable_Name = f"V_A"

                # Control for Limits
                if V_Variable_Name is not None and V_Value > Limits.INSTANT_VOLTAGE_MIN and V_Value < Limits.INSTANT_VOLTAGE_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, V_Variable_Name, V_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {V_Variable_Name} : {V_Value}")
        else :

            # Control for Phase R Instant Voltage
            if Message.V_R is not None and Message.V_R > Limits.INSTANT_VOLTAGE_MIN and Message.V_R < Limits.INSTANT_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "V_R", Message.V_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> V_R : {Message.V_R}")

            # Control for Phase S Instant Voltage
            if Message.V_S is not None and Message.V_S > Limits.INSTANT_VOLTAGE_MIN and Message.V_S < Limits.INSTANT_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "V_S", Message.V_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> V_S : {Message.V_S}")

            # Control for Phase T Instant Voltage
            if Message.V_T is not None and Message.V_T > Limits.INSTANT_VOLTAGE_MIN and Message.V_T < Limits.INSTANT_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "V_T", Message.V_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> V_T : {Message.V_T}")

            # Control for Instant Voltage Average
            if Message.V_A is not None and Message.V_A > Limits.INSTANT_VOLTAGE_MIN and Message.V_A < Limits.INSTANT_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "V_A", Message.V_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> V_A : {Message.V_A}")




















        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Close Database
    DB_Module.close()
