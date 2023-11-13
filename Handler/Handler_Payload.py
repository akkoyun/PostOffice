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

        # Control for Instant Voltage (Array)
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

        # Control for Instant Voltage (Single)
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

        # Control for RMS Voltage (Array)
        if Message.VRMS is not None:

            # Loop Through Measurements
            for index, VRMS_Value in enumerate(Message.VRMS):

                # Set Dynamic Variable Name
                if index == 0: VRMS_Variable_Name = f"VRMS_R"
                if index == 1: VRMS_Variable_Name = f"VRMS_S"
                if index == 2: VRMS_Variable_Name = f"VRMS_T"
                if index == 3: VRMS_Variable_Name = f"VRMS_A"

                # Control for Limits
                if VRMS_Variable_Name is not None and VRMS_Value > Limits.RMS_VOLTAGE_MIN and VRMS_Value < Limits.RMS_VOLTAGE_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, VRMS_Variable_Name, VRMS_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {VRMS_Variable_Name} : {VRMS_Value}")

        # Control for RMS Voltage (Single)
        else :

            # Control for Phase R RMS Voltage
            if Message.VRMS_R is not None and Message.VRMS_R > Limits.RMS_VOLTAGE_MIN and Message.VRMS_R < Limits.RMS_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VRMS_R", Message.VRMS_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VRMS_R : {Message.VRMS_R}")

            # Control for Phase S RMS Voltage
            if Message.VRMS_S is not None and Message.VRMS_S > Limits.RMS_VOLTAGE_MIN and Message.VRMS_S < Limits.RMS_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VRMS_S", Message.VRMS_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VRMS_S : {Message.VRMS_S}")

            # Control for Phase T RMS Voltage
            if Message.VRMS_T is not None and Message.VRMS_T > Limits.RMS_VOLTAGE_MIN and Message.VRMS_T < Limits.RMS_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VRMS_T", Message.VRMS_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VRMS_T : {Message.VRMS_T}")

            # Control for RMS Voltage Average
            if Message.VRMS_A is not None and Message.VRMS_A > Limits.RMS_VOLTAGE_MIN and Message.VRMS_A < Limits.RMS_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VRMS_A", Message.VRMS_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VRMS_A : {Message.VRMS_A}")

        # Control for Fundamental Voltage (Array)
        if Message.VFun is not None:

            # Loop Through Measurements
            for index, VFun_Value in enumerate(Message.VFun):

                # Set Dynamic Variable Name
                if index == 0: VFun_Variable_Name = f"VFun_R"
                if index == 1: VFun_Variable_Name = f"VFun_S"
                if index == 2: VFun_Variable_Name = f"VFun_T"
                if index == 3: VFun_Variable_Name = f"VFun_A"

                # Control for Limits
                if VFun_Variable_Name is not None and VFun_Value > Limits.FUNDAMENTAL_VOLTAGE_MIN and VFun_Value < Limits.FUNDAMENTAL_VOLTAGE_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, VFun_Variable_Name, VFun_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {VFun_Variable_Name} : {VFun_Value}")

        # Control for Fundamental Voltage (Single)
        else :

            # Control for Phase R Fundamental Voltage
            if Message.VFun_R is not None and Message.VFun_R > Limits.FUNDAMENTAL_VOLTAGE_MIN and Message.VFun_R < Limits.FUNDAMENTAL_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VFun_R", Message.VFun_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VFun_R : {Message.VFun_R}")

            # Control for Phase S Fundamental Voltage
            if Message.VFun_S is not None and Message.VFun_S > Limits.FUNDAMENTAL_VOLTAGE_MIN and Message.VFun_S < Limits.FUNDAMENTAL_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VFun_S", Message.VFun_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VFun_S : {Message.VFun_S}")

            # Control for Phase T Fundamental Voltage
            if Message.VFun_T is not None and Message.VFun_T > Limits.FUNDAMENTAL_VOLTAGE_MIN and Message.VFun_T < Limits.FUNDAMENTAL_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VFun_T", Message.VFun_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VFun_T : {Message.VFun_T}")

            # Control for Fundamental Voltage Average
            if Message.VFun_A is not None and Message.VFun_A > Limits.FUNDAMENTAL_VOLTAGE_MIN and Message.VFun_A < Limits.FUNDAMENTAL_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VFun_A", Message.VFun_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VFun_A : {Message.VFun_A}")

        # Control for Harmonic Voltage (Array)
        if Message.VHarm is not None:

            # Loop Through Measurements
            for index, VHarm_Value in enumerate(Message.VHarm):

                # Set Dynamic Variable Name
                if index == 0: VHarm_Variable_Name = f"VHarm_R"
                if index == 1: VHarm_Variable_Name = f"VHarm_S"
                if index == 2: VHarm_Variable_Name = f"VHarm_T"
                if index == 3: VHarm_Variable_Name = f"VHarm_A"

                # Control for Limits
                if VHarm_Variable_Name is not None and VHarm_Value > Limits.HARMONIC_VOLTAGE_MIN and VHarm_Value < Limits.HARMONIC_VOLTAGE_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, VHarm_Variable_Name, VHarm_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {VHarm_Variable_Name} : {VHarm_Value}")
        
        # Control for Harmonic Voltage (Single)
        else :

            # Control for Phase R Harmonic Voltage
            if Message.VHarm_R is not None and Message.VHarm_R > Limits.HARMONIC_VOLTAGE_MIN and Message.VHarm_R < Limits.HARMONIC_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VHarm_R", Message.VHarm_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VHarm_R : {Message.VHarm_R}")

            # Control for Phase S Harmonic Voltage
            if Message.VHarm_S is not None and Message.VHarm_S > Limits.HARMONIC_VOLTAGE_MIN and Message.VHarm_S < Limits.HARMONIC_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VHarm_S", Message.VHarm_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VHarm_S : {Message.VHarm_S}")

            # Control for Phase T Harmonic Voltage
            if Message.VHarm_T is not None and Message.VHarm_T > Limits.HARMONIC_VOLTAGE_MIN and Message.VHarm_T < Limits.HARMONIC_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VHarm_T", Message.VHarm_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VHarm_T : {Message.VHarm_T}")

            # Control for Harmonic Voltage Average
            if Message.VHarm_A is not None and Message.VHarm_A > Limits.HARMONIC_VOLTAGE_MIN and Message.VHarm_A < Limits.HARMONIC_VOLTAGE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "VHarm_A", Message.VHarm_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> VHarm_A : {Message.VHarm_A}")

        # Control for Instant Current (Array)
        if Message.I is not None:

            # Loop Through Measurements
            for index, I_Value in enumerate(Message.I):

                # Set Dynamic Variable Name
                if index == 0: I_Variable_Name = f"I_R"
                if index == 1: I_Variable_Name = f"I_S"
                if index == 2: I_Variable_Name = f"I_T"
                if index == 3: I_Variable_Name = f"I_A"

                # Control for Limits
                if I_Variable_Name is not None and I_Value > Limits.INSTANT_CURRENT_MIN and I_Value < Limits.INSTANT_CURRENT_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, I_Variable_Name, I_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {I_Variable_Name} : {I_Value}")
        
        # Control for Instant Current (Single)
        else :

            # Control for Phase R Instant Current
            if Message.I_R is not None and Message.I_R > Limits.INSTANT_CURRENT_MIN and Message.I_R < Limits.INSTANT_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "I_R", Message.I_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> I_R : {Message.I_R}")

            # Control for Phase S Instant Current
            if Message.I_S is not None and Message.I_S > Limits.INSTANT_CURRENT_MIN and Message.I_S < Limits.INSTANT_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "I_S", Message.I_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> I_S : {Message.I_S}")

            # Control for Phase T Instant Current
            if Message.I_T is not None and Message.I_T > Limits.INSTANT_CURRENT_MIN and Message.I_T < Limits.INSTANT_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "I_T", Message.I_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> I_T : {Message.I_T}")

            # Control for Instant Current Average
            if Message.I_A is not None and Message.I_A > Limits.INSTANT_CURRENT_MIN and Message.I_A < Limits.INSTANT_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "I_A", Message.I_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> I_A : {Message.I_A}")

        # Control for Peak Current (Array)
        if Message.IP is not None:

            # Loop Through Measurements
            for index, IP_Value in enumerate(Message.IP):

                # Set Dynamic Variable Name
                if index == 0: IP_Variable_Name = f"IP_R"
                if index == 1: IP_Variable_Name = f"IP_S"
                if index == 2: IP_Variable_Name = f"IP_T"
                if index == 3: IP_Variable_Name = f"IP_A"

                # Control for Limits
                if IP_Variable_Name is not None and IP_Value > Limits.PEAK_CURRENT_MIN and IP_Value < Limits.PEAK_CURRENT_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, IP_Variable_Name, IP_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {IP_Variable_Name} : {IP_Value}")
        
        # Control for Peak Current (Single)
        else :

            # Control for Phase R Peak Current
            if Message.IP_R is not None and Message.IP_R > Limits.PEAK_CURRENT_MIN and Message.IP_R < Limits.PEAK_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IP_R", Message.IP_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IP_R : {Message.IP_R}")

            # Control for Phase S Peak Current
            if Message.IP_S is not None and Message.IP_S > Limits.PEAK_CURRENT_MIN and Message.IP_S < Limits.PEAK_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IP_S", Message.IP_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IP_S : {Message.IP_S}")

            # Control for Phase T Peak Current
            if Message.IP_T is not None and Message.IP_T > Limits.PEAK_CURRENT_MIN and Message.IP_T < Limits.PEAK_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IP_T", Message.IP_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IP_T : {Message.IP_T}")

            # Control for Peak Current Average
            if Message.IP_A is not None and Message.IP_A > Limits.PEAK_CURRENT_MIN and Message.IP_A < Limits.PEAK_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IP_A", Message.IP_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IP_A : {Message.IP_A}")

        # Control for RMS Current (Array)
        if Message.IRMS is not None:

            # Loop Through Measurements
            for index, IRMS_Value in enumerate(Message.IRMS):

                # Set Dynamic Variable Name
                if index == 0: IRMS_Variable_Name = f"IRMS_R"
                if index == 1: IRMS_Variable_Name = f"IRMS_S"
                if index == 2: IRMS_Variable_Name = f"IRMS_T"
                if index == 3: IRMS_Variable_Name = f"IRMS_A"

                # Control for Limits
                if IRMS_Variable_Name is not None and IRMS_Value > Limits.RMS_CURRENT_MIN and IRMS_Value < Limits.RMS_CURRENT_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, IRMS_Variable_Name, IRMS_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {IRMS_Variable_Name} : {IRMS_Value}")
        
        # Control for RMS Current (Single)
        else :

            # Control for Phase R RMS Current
            if Message.IRMS_R is not None and Message.IRMS_R > Limits.RMS_CURRENT_MIN and Message.IRMS_R < Limits.RMS_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IRMS_R", Message.IRMS_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IRMS_R : {Message.IRMS_R}")

            # Control for Phase S RMS Current
            if Message.IRMS_S is not None and Message.IRMS_S > Limits.RMS_CURRENT_MIN and Message.IRMS_S < Limits.RMS_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IRMS_S", Message.IRMS_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IRMS_S : {Message.IRMS_S}")

            # Control for Phase T RMS Current
            if Message.IRMS_T is not None and Message.IRMS_T > Limits.RMS_CURRENT_MIN and Message.IRMS_T < Limits.RMS_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IRMS_T", Message.IRMS_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IRMS_T : {Message.IRMS_T}")

            # Control for RMS Current Average
            if Message.IRMS_A is not None and Message.IRMS_A > Limits.RMS_CURRENT_MIN and Message.IRMS_A < Limits.RMS_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IRMS_A", Message.IRMS_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IRMS_A : {Message.IRMS_A}")

        # Control for Fundamental Current (Array)
        if Message.IFun is not None:

            # Loop Through Measurements
            for index, IFun_Value in enumerate(Message.IFun):

                # Set Dynamic Variable Name
                if index == 0: IFun_Variable_Name = f"IFun_R"
                if index == 1: IFun_Variable_Name = f"IFun_S"
                if index == 2: IFun_Variable_Name = f"IFun_T"
                if index == 3: IFun_Variable_Name = f"IFun_A"

                # Control for Limits
                if IFun_Variable_Name is not None and IFun_Value > Limits.FUNDAMENTAL_CURRENT_MIN and IFun_Value < Limits.FUNDAMENTAL_CURRENT_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, IFun_Variable_Name, IFun_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {IFun_Variable_Name} : {IFun_Value}")

        # Control for Fundamental Current (Single)
        else :

            # Control for Phase R Fundamental Current
            if Message.IFun_R is not None and Message.IFun_R > Limits.FUNDAMENTAL_CURRENT_MIN and Message.IFun_R < Limits.FUNDAMENTAL_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IFun_R", Message.IFun_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IFun_R : {Message.IFun_R}")

            # Control for Phase S Fundamental Current
            if Message.IFun_S is not None and Message.IFun_S > Limits.FUNDAMENTAL_CURRENT_MIN and Message.IFun_S < Limits.FUNDAMENTAL_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IFun_S", Message.IFun_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IFun_S : {Message.IFun_S}")

            # Control for Phase T Fundamental Current
            if Message.IFun_T is not None and Message.IFun_T > Limits.FUNDAMENTAL_CURRENT_MIN and Message.IFun_T < Limits.FUNDAMENTAL_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IFun_T", Message.IFun_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IFun_T : {Message.IFun_T}")

            # Control for Fundamental Current Average
            if Message.IFun_A is not None and Message.IFun_A > Limits.FUNDAMENTAL_CURRENT_MIN and Message.IFun_A < Limits.FUNDAMENTAL_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IFun_A", Message.IFun_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IFun_A : {Message.IFun_A}")

        # Control for Harmonic Current (Array)
        if Message.IHarm is not None:

            # Loop Through Measurements
            for index, IHarm_Value in enumerate(Message.IHarm):

                # Set Dynamic Variable Name
                if index == 0: IHarm_Variable_Name = f"IHarm_R"
                if index == 1: IHarm_Variable_Name = f"IHarm_S"
                if index == 2: IHarm_Variable_Name = f"IHarm_T"
                if index == 3: IHarm_Variable_Name = f"IHarm_A"

                # Control for Limits
                if IHarm_Variable_Name is not None and IHarm_Value > Limits.HARMONIC_CURRENT_MIN and IHarm_Value < Limits.HARMONIC_CURRENT_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, IHarm_Variable_Name, IHarm_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {IHarm_Variable_Name} : {IHarm_Value}")

        # Control for Harmonic Current (Single)
        else :

            # Control for Phase R Harmonic Current
            if Message.IHarm_R is not None and Message.IHarm_R > Limits.HARMONIC_CURRENT_MIN and Message.IHarm_R < Limits.HARMONIC_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IHarm_R", Message.IHarm_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IHarm_R : {Message.IHarm_R}")

            # Control for Phase S Harmonic Current
            if Message.IHarm_S is not None and Message.IHarm_S > Limits.HARMONIC_CURRENT_MIN and Message.IHarm_S < Limits.HARMONIC_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IHarm_S", Message.IHarm_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IHarm_S : {Message.IHarm_S}")

            # Control for Phase T Harmonic Current
            if Message.IHarm_T is not None and Message.IHarm_T > Limits.HARMONIC_CURRENT_MIN and Message.IHarm_T < Limits.HARMONIC_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IHarm_T", Message.IHarm_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IHarm_T : {Message.IHarm_T}")

            # Control for Harmonic Current Average
            if Message.IHarm_A is not None and Message.IHarm_A > Limits.HARMONIC_CURRENT_MIN and Message.IHarm_A < Limits.HARMONIC_CURRENT_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "IHarm_A", Message.IHarm_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> IHarm_A : {Message.IHarm_A}")
                                         
                






















        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Close Database
    DB_Module.close()
