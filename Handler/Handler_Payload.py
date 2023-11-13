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

        # Control for PCB Temperature
        if Message.PCB_T is not None and Message.PCB_T > Limits.PCB_TEMPERATURE_MIN and Message.PCB_T < Limits.PCB_TEMPERATURE_MAX:

            # Set PCB_T
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PCB_T", Message.PCB_T)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> PCB_T : {Message.PCB_T}")

        # Control for PCB Humidity
        if Message.PCB_H is not None and Message.PCB_H > Limits.PCB_HUMIDITY_MIN and Message.PCB_H < Limits.PCB_HUMIDITY_MAX:

            # Set PCB_H
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PCB_H", Message.PCB_H)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> PCB_H : {Message.PCB_H}")

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
                                         
        # Control for Active Power (Array)
        if Message.P is not None:

            # Loop Through Measurements
            for index, P_Value in enumerate(Message.P):

                # Set Dynamic Variable Name
                if index == 0: P_Variable_Name = f"P_R"
                if index == 1: P_Variable_Name = f"P_S"
                if index == 2: P_Variable_Name = f"P_T"
                if index == 3: P_Variable_Name = f"P_A"

                # Control for Limits
                if P_Variable_Name is not None and P_Value > Limits.ACTIVE_POWER_MIN and P_Value < Limits.ACTIVE_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, P_Variable_Name, P_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {P_Variable_Name} : {P_Value}")

        # Control for Active Power (Single)
        else :

            # Control for Phase R Active Power
            if Message.P_R is not None and Message.P_R > Limits.ACTIVE_POWER_MIN and Message.P_R < Limits.ACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "P_R", Message.P_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> P_R : {Message.P_R}")

            # Control for Phase S Active Power
            if Message.P_S is not None and Message.P_S > Limits.ACTIVE_POWER_MIN and Message.P_S < Limits.ACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "P_S", Message.P_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> P_S : {Message.P_S}")

            # Control for Phase T Active Power
            if Message.P_T is not None and Message.P_T > Limits.ACTIVE_POWER_MIN and Message.P_T < Limits.ACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "P_T", Message.P_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> P_T : {Message.P_T}")

            # Control for Active Power Average
            if Message.P_A is not None and Message.P_A > Limits.ACTIVE_POWER_MIN and Message.P_A < Limits.ACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "P_A", Message.P_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> P_A : {Message.P_A}")

        # Control for Reactive Power (Array)
        if Message.Q is not None:

            # Loop Through Measurements
            for index, Q_Value in enumerate(Message.Q):

                # Set Dynamic Variable Name
                if index == 0: Q_Variable_Name = f"Q_R"
                if index == 1: Q_Variable_Name = f"Q_S"
                if index == 2: Q_Variable_Name = f"Q_T"
                if index == 3: Q_Variable_Name = f"Q_A"

                # Control for Limits
                if Q_Variable_Name is not None and Q_Value > Limits.REACTIVE_POWER_MIN and Q_Value < Limits.REACTIVE_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, Q_Variable_Name, Q_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {Q_Variable_Name} : {Q_Value}")

        # Control for Reactive Power (Single)
        else :

            # Control for Phase R Reactive Power
            if Message.Q_R is not None and Message.Q_R > Limits.REACTIVE_POWER_MIN and Message.Q_R < Limits.REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Q_R", Message.Q_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> Q_R : {Message.Q_R}")

            # Control for Phase S Reactive Power
            if Message.Q_S is not None and Message.Q_S > Limits.REACTIVE_POWER_MIN and Message.Q_S < Limits.REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Q_S", Message.Q_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> Q_S : {Message.Q_S}")

            # Control for Phase T Reactive Power
            if Message.Q_T is not None and Message.Q_T > Limits.REACTIVE_POWER_MIN and Message.Q_T < Limits.REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Q_T", Message.Q_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> Q_T : {Message.Q_T}")

            # Control for Reactive Power Average
            if Message.Q_A is not None and Message.Q_A > Limits.REACTIVE_POWER_MIN and Message.Q_A < Limits.REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Q_A", Message.Q_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> Q_A : {Message.Q_A}")

        # Control for Apparent Power (Array)
        if Message.S is not None:

            # Loop Through Measurements
            for index, S_Value in enumerate(Message.S):

                # Set Dynamic Variable Name
                if index == 0: S_Variable_Name = f"S_R"
                if index == 1: S_Variable_Name = f"S_S"
                if index == 2: S_Variable_Name = f"S_T"
                if index == 3: S_Variable_Name = f"S_A"

                # Control for Limits
                if S_Variable_Name is not None and S_Value > Limits.APPARENT_POWER_MIN and S_Value < Limits.APPARENT_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, S_Variable_Name, S_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {S_Variable_Name} : {S_Value}")

        # Control for Apparent Power (Single)
        else :

            # Control for Phase R Apparent Power
            if Message.S_R is not None and Message.S_R > Limits.APPARENT_POWER_MIN and Message.S_R < Limits.APPARENT_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "S_R", Message.S_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> S_R : {Message.S_R}")

            # Control for Phase S Apparent Power
            if Message.S_S is not None and Message.S_S > Limits.APPARENT_POWER_MIN and Message.S_S < Limits.APPARENT_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "S_S", Message.S_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> S_S : {Message.S_S}")

            # Control for Phase T Apparent Power
            if Message.S_T is not None and Message.S_T > Limits.APPARENT_POWER_MIN and Message.S_T < Limits.APPARENT_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "S_T", Message.S_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> S_T : {Message.S_T}")

            # Control for Apparent Power Average
            if Message.S_A is not None and Message.S_A > Limits.APPARENT_POWER_MIN and Message.S_A < Limits.APPARENT_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "S_A", Message.S_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> S_A : {Message.S_A}")

        # Control for Fundamental Reactive Power (Array)
        if Message.QFun is not None:

            # Loop Through Measurements
            for index, QFun_Value in enumerate(Message.QFun):

                # Set Dynamic Variable Name
                if index == 0: QFun_Variable_Name = f"QFun_R"
                if index == 1: QFun_Variable_Name = f"QFun_S"
                if index == 2: QFun_Variable_Name = f"QFun_T"
                if index == 3: QFun_Variable_Name = f"QFun_A"

                # Control for Limits
                if QFun_Variable_Name is not None and QFun_Value > Limits.FUNDAMENTAL_REACTIVE_POWER_MIN and QFun_Value < Limits.FUNDAMENTAL_REACTIVE_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, QFun_Variable_Name, QFun_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {QFun_Variable_Name} : {QFun_Value}")

        # Control for Fundamental Reactive Power (Single)
        else :

            # Control for Phase R Fundamental Reactive Power
            if Message.QFun_R is not None and Message.QFun_R > Limits.FUNDAMENTAL_REACTIVE_POWER_MIN and Message.QFun_R < Limits.FUNDAMENTAL_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QFun_R", Message.QFun_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QFun_R : {Message.QFun_R}")

            # Control for Phase S Fundamental Reactive Power
            if Message.QFun_S is not None and Message.QFun_S > Limits.FUNDAMENTAL_REACTIVE_POWER_MIN and Message.QFun_S < Limits.FUNDAMENTAL_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QFun_S", Message.QFun_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QFun_S : {Message.QFun_S}")

            # Control for Phase T Fundamental Reactive Power
            if Message.QFun_T is not None and Message.QFun_T > Limits.FUNDAMENTAL_REACTIVE_POWER_MIN and Message.QFun_T < Limits.FUNDAMENTAL_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QFun_T", Message.QFun_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QFun_T : {Message.QFun_T}")

            # Control for Fundamental Reactive Power Average
            if Message.QFun_A is not None and Message.QFun_A > Limits.FUNDAMENTAL_REACTIVE_POWER_MIN and Message.QFun_A < Limits.FUNDAMENTAL_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QFun_A", Message.QFun_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QFun_A : {Message.QFun_A}")

        # Control for Harmonic Reactive Power (Array)
        if Message.QHarm is not None:

            # Loop Through Measurements
            for index, QHarm_Value in enumerate(Message.QHarm):

                # Set Dynamic Variable Name
                if index == 0: QHarm_Variable_Name = f"QHarm_R"
                if index == 1: QHarm_Variable_Name = f"QHarm_S"
                if index == 2: QHarm_Variable_Name = f"QHarm_T"
                if index == 3: QHarm_Variable_Name = f"QHarm_A"

                # Control for Limits
                if QHarm_Variable_Name is not None and QHarm_Value > Limits.HARMONIC_REACTIVE_POWER_MIN and QHarm_Value < Limits.HARMONIC_REACTIVE_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, QHarm_Variable_Name, QHarm_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {QHarm_Variable_Name} : {QHarm_Value}")

        # Control for Harmonic Reactive Power (Single)
        else :

            # Control for Phase R Harmonic Reactive Power
            if Message.QHarm_R is not None and Message.QHarm_R > Limits.HARMONIC_REACTIVE_POWER_MIN and Message.QHarm_R < Limits.HARMONIC_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QHarm_R", Message.QHarm_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QHarm_R : {Message.QHarm_R}")

            # Control for Phase S Harmonic Reactive Power
            if Message.QHarm_S is not None and Message.QHarm_S > Limits.HARMONIC_REACTIVE_POWER_MIN and Message.QHarm_S < Limits.HARMONIC_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QHarm_S", Message.QHarm_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QHarm_S : {Message.QHarm_S}")

            # Control for Phase T Harmonic Reactive Power
            if Message.QHarm_T is not None and Message.QHarm_T > Limits.HARMONIC_REACTIVE_POWER_MIN and Message.QHarm_T < Limits.HARMONIC_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QHarm_T", Message.QHarm_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QHarm_T : {Message.QHarm_T}")

            # Control for Harmonic Reactive Power Average
            if Message.QHarm_A is not None and Message.QHarm_A > Limits.HARMONIC_REACTIVE_POWER_MIN and Message.QHarm_A < Limits.HARMONIC_REACTIVE_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "QHarm_A", Message.QHarm_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> QHarm_A : {Message.QHarm_A}")

        # Control for Fundamental Power (Array)
        if Message.PFun is not None:

            # Loop Through Measurements
            for index, PFun_Value in enumerate(Message.PFun):

                # Set Dynamic Variable Name
                if index == 0: PFun_Variable_Name = f"PFun_R"
                if index == 1: PFun_Variable_Name = f"PFun_S"
                if index == 2: PFun_Variable_Name = f"PFun_T"
                if index == 3: PFun_Variable_Name = f"PFun_A"

                # Control for Limits
                if PFun_Variable_Name is not None and PFun_Value > Limits.FUNDAMENTAL_POWER_MIN and PFun_Value < Limits.FUNDAMENTAL_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, PFun_Variable_Name, PFun_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {PFun_Variable_Name} : {PFun_Value}")

        # Control for Fundamental Power (Single)
        else :

            # Control for Phase R Fundamental Power
            if Message.PFun_R is not None and Message.PFun_R > Limits.FUNDAMENTAL_POWER_MIN and Message.PFun_R < Limits.FUNDAMENTAL_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PFun_R", Message.PFun_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PFun_R : {Message.PFun_R}")

            # Control for Phase S Fundamental Power
            if Message.PFun_S is not None and Message.PFun_S > Limits.FUNDAMENTAL_POWER_MIN and Message.PFun_S < Limits.FUNDAMENTAL_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PFun_S", Message.PFun_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PFun_S : {Message.PFun_S}")

            # Control for Phase T Fundamental Power
            if Message.PFun_T is not None and Message.PFun_T > Limits.FUNDAMENTAL_POWER_MIN and Message.PFun_T < Limits.FUNDAMENTAL_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PFun_T", Message.PFun_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PFun_T : {Message.PFun_T}")

            # Control for Fundamental Power Average
            if Message.PFun_A is not None and Message.PFun_A > Limits.FUNDAMENTAL_POWER_MIN and Message.PFun_A < Limits.FUNDAMENTAL_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PFun_A", Message.PFun_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PFun_A : {Message.PFun_A}")

        # Control for Harmonic Power (Array)
        if Message.PHarm is not None:

            # Loop Through Measurements
            for index, PHarm_Value in enumerate(Message.PHarm):

                # Set Dynamic Variable Name
                if index == 0: PHarm_Variable_Name = f"PHarm_R"
                if index == 1: PHarm_Variable_Name = f"PHarm_S"
                if index == 2: PHarm_Variable_Name = f"PHarm_T"
                if index == 3: PHarm_Variable_Name = f"PHarm_A"

                # Control for Limits
                if PHarm_Variable_Name is not None and PHarm_Value > Limits.HARMONIC_POWER_MIN and PHarm_Value < Limits.HARMONIC_POWER_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, PHarm_Variable_Name, PHarm_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {PHarm_Variable_Name} : {PHarm_Value}")

        # Control for Harmonic Power (Single)
        else :

            # Control for Phase R Harmonic Power
            if Message.PHarm_R is not None and Message.PHarm_R > Limits.HARMONIC_POWER_MIN and Message.PHarm_R < Limits.HARMONIC_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PHarm_R", Message.PHarm_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PHarm_R : {Message.PHarm_R}")

            # Control for Phase S Harmonic Power
            if Message.PHarm_S is not None and Message.PHarm_S > Limits.HARMONIC_POWER_MIN and Message.PHarm_S < Limits.HARMONIC_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PHarm_S", Message.PHarm_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PHarm_S : {Message.PHarm_S}")

            # Control for Phase T Harmonic Power
            if Message.PHarm_T is not None and Message.PHarm_T > Limits.HARMONIC_POWER_MIN and Message.PHarm_T < Limits.HARMONIC_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PHarm_T", Message.PHarm_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PHarm_T : {Message.PHarm_T}")

            # Control for Harmonic Power Average
            if Message.PHarm_A is not None and Message.PHarm_A > Limits.HARMONIC_POWER_MIN and Message.PHarm_A < Limits.HARMONIC_POWER_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PHarm_A", Message.PHarm_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PHarm_A : {Message.PHarm_A}")

        # Control for Fundamental Volt Ampere (Array)
        if Message.FunVA is not None:

            # Loop Through Measurements
            for index, FunVA_Value in enumerate(Message.FunVA):

                # Set Dynamic Variable Name
                if index == 0: FunVA_Variable_Name = f"FunVA_R"
                if index == 1: FunVA_Variable_Name = f"FunVA_S"
                if index == 2: FunVA_Variable_Name = f"FunVA_T"
                if index == 3: FunVA_Variable_Name = f"FunVA_A"

                # Control for Limits
                if FunVA_Variable_Name is not None and FunVA_Value > Limits.FUNDAMENTAL_VOLT_AMPERE_MIN and FunVA_Value < Limits.FUNDAMENTAL_VOLT_AMPERE_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, FunVA_Variable_Name, FunVA_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {FunVA_Variable_Name} : {FunVA_Value}")

        # Control for Fundamental Volt Ampere (Single)
        else :

            # Control for Phase R Fundamental Volt Ampere
            if Message.FunVA_R is not None and Message.FunVA_R > Limits.FUNDAMENTAL_VOLT_AMPERE_MIN and Message.FunVA_R < Limits.FUNDAMENTAL_VOLT_AMPERE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "FunVA_R", Message.FunVA_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> FunVA_R : {Message.FunVA_R}")

            # Control for Phase S Fundamental Volt Ampere
            if Message.FunVA_S is not None and Message.FunVA_S > Limits.FUNDAMENTAL_VOLT_AMPERE_MIN and Message.FunVA_S < Limits.FUNDAMENTAL_VOLT_AMPERE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "FunVA_S", Message.FunVA_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> FunVA_S : {Message.FunVA_S}")

            # Control for Phase T Fundamental Volt Ampere
            if Message.FunVA_T is not None and Message.FunVA_T > Limits.FUNDAMENTAL_VOLT_AMPERE_MIN and Message.FunVA_T < Limits.FUNDAMENTAL_VOLT_AMPERE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "FunVA_T", Message.FunVA_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> FunVA_T : {Message.FunVA_T}")

            # Control for Fundamental Volt Ampere Average
            if Message.FunVA_A is not None and Message.FunVA_A > Limits.FUNDAMENTAL_VOLT_AMPERE_MIN and Message.FunVA_A < Limits.FUNDAMENTAL_VOLT_AMPERE_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "FunVA_A", Message.FunVA_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> FunVA_A : {Message.FunVA_A}")

        # Control for Power Factor (Array)
        if Message.PF is not None:

            # Loop Through Measurements
            for index, PF_Value in enumerate(Message.PF):

                # Set Dynamic Variable Name
                if index == 0: PF_Variable_Name = f"PF_R"
                if index == 1: PF_Variable_Name = f"PF_S"
                if index == 2: PF_Variable_Name = f"PF_T"
                if index == 3: PF_Variable_Name = f"PF_A"

                # Control for Limits
                if PF_Variable_Name is not None and PF_Value > Limits.POWER_FACTOR_MIN and PF_Value < Limits.POWER_FACTOR_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, PF_Variable_Name, PF_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {PF_Variable_Name} : {PF_Value}")

        # Control for Power Factor (Single)
        else :

            # Control for Phase R Power Factor
            if Message.PF_R is not None and Message.PF_R > Limits.POWER_FACTOR_MIN and Message.PF_R < Limits.POWER_FACTOR_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PF_R", Message.PF_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PF_R : {Message.PF_R}")

            # Control for Phase S Power Factor
            if Message.PF_S is not None and Message.PF_S > Limits.POWER_FACTOR_MIN and Message.PF_S < Limits.POWER_FACTOR_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PF_S", Message.PF_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PF_S : {Message.PF_S}")

            # Control for Phase T Power Factor
            if Message.PF_T is not None and Message.PF_T > Limits.POWER_FACTOR_MIN and Message.PF_T < Limits.POWER_FACTOR_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PF_T", Message.PF_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PF_T : {Message.PF_T}")

            # Control for Power Factor Average
            if Message.PF_A is not None and Message.PF_A > Limits.POWER_FACTOR_MIN and Message.PF_A < Limits.POWER_FACTOR_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "PF_A", Message.PF_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> PF_A : {Message.PF_A}")

        # Control for Active Energy (Array)
        if Message.AE is not None:

            # Loop Through Measurements
            for index, AE_Value in enumerate(Message.AE):

                # Set Dynamic Variable Name
                if index == 0: AE_Variable_Name = f"AE_R"
                if index == 1: AE_Variable_Name = f"AE_S"
                if index == 2: AE_Variable_Name = f"AE_T"
                if index == 3: AE_Variable_Name = f"AE_A"
                if index == 4: AE_Variable_Name = f"AE_TOT"

                # Control for Limits
                if AE_Variable_Name is not None and AE_Value > Limits.ACTIVE_ENERGY_MIN and AE_Value < Limits.ACTIVE_ENERGY_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, AE_Variable_Name, AE_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {AE_Variable_Name} : {AE_Value}")

        # Control for Active Energy (Single)
        else :

            # Control for Phase R Active Energy
            if Message.AE_R is not None and Message.AE_R > Limits.ACTIVE_ENERGY_MIN and Message.AE_R < Limits.ACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AE_R", Message.AE_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AE_R : {Message.AE_R}")

            # Control for Phase S Active Energy
            if Message.AE_S is not None and Message.AE_S > Limits.ACTIVE_ENERGY_MIN and Message.AE_S < Limits.ACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AE_S", Message.AE_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AE_S : {Message.AE_S}")

            # Control for Phase T Active Energy
            if Message.AE_T is not None and Message.AE_T > Limits.ACTIVE_ENERGY_MIN and Message.AE_T < Limits.ACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AE_T", Message.AE_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AE_T : {Message.AE_T}")

            # Control for Active Energy Average
            if Message.AE_A is not None and Message.AE_A > Limits.ACTIVE_ENERGY_MIN and Message.AE_A < Limits.ACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AE_A", Message.AE_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AE_A : {Message.AE_A}")

            # Control for Total Active Energy
            if Message.AE_TOT is not None and Message.AE_TOT > Limits.ACTIVE_ENERGY_MIN and Message.AE_TOT < Limits.ACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "AE_TOT", Message.AE_TOT)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> AE_TOT : {Message.AE_TOT}")

        # Control for Reactive Energy Leading (Array)
        if Message.RE_L is not None:

            # Loop Through Measurements
            for index, RE_L_Value in enumerate(Message.RE_L):

                # Set Dynamic Variable Name
                if index == 0: RE_L_Variable_Name = f"RE_L_R"
                if index == 1: RE_L_Variable_Name = f"RE_L_S"
                if index == 2: RE_L_Variable_Name = f"RE_L_T"
                if index == 3: RE_L_Variable_Name = f"RE_L_A"
                if index == 4: RE_L_Variable_Name = f"RE_L_TOT"

                # Control for Limits
                if RE_L_Variable_Name is not None and RE_L_Value > Limits.REACTIVE_ENERGY_MIN and RE_L_Value < Limits.REACTIVE_ENERGY_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, RE_L_Variable_Name, RE_L_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {RE_L_Variable_Name} : {RE_L_Value}")

        # Control for Reactive Energy Leading (Single)
        else :

            # Control for Phase R Reactive Energy Leading
            if Message.RE_L_R is not None and Message.RE_L_R > Limits.REACTIVE_ENERGY_MIN and Message.RE_L_R < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_L_R", Message.RE_L_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_L_R : {Message.RE_L_R}")

            # Control for Phase S Reactive Energy Leading
            if Message.RE_L_S is not None and Message.RE_L_S > Limits.REACTIVE_ENERGY_MIN and Message.RE_L_S < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_L_S", Message.RE_L_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_L_S : {Message.RE_L_S}")

            # Control for Phase T Reactive Energy Leading
            if Message.RE_L_T is not None and Message.RE_L_T > Limits.REACTIVE_ENERGY_MIN and Message.RE_L_T < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_L_T", Message.RE_L_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_L_T : {Message.RE_L_T}")

            # Control for Reactive Energy Leading Average
            if Message.RE_L_A is not None and Message.RE_L_A > Limits.REACTIVE_ENERGY_MIN and Message.RE_L_A < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_L_A", Message.RE_L_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_L_A : {Message.RE_L_A}")

            # Control for Total Reactive Energy Leading
            if Message.RE_L_TOT is not None and Message.RE_L_TOT > Limits.REACTIVE_ENERGY_MIN and Message.RE_L_TOT < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_L_TOT", Message.RE_L_TOT)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_L_TOT : {Message.RE_L_TOT}")

        # Control for Reactive Energy Lagging (Array)
        if Message.RE_G is not None:

            # Loop Through Measurements
            for index, RE_G_Value in enumerate(Message.RE_G):

                # Set Dynamic Variable Name
                if index == 0: RE_G_Variable_Name = f"RE_G_R"
                if index == 1: RE_G_Variable_Name = f"RE_G_S"
                if index == 2: RE_G_Variable_Name = f"RE_G_T"
                if index == 3: RE_G_Variable_Name = f"RE_G_A"
                if index == 4: RE_G_Variable_Name = f"RE_G_TOT"

                # Control for Limits
                if RE_G_Variable_Name is not None and RE_G_Value > Limits.REACTIVE_ENERGY_MIN and RE_G_Value < Limits.REACTIVE_ENERGY_MAX:

                    # Set ST
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, RE_G_Variable_Name, RE_G_Value)

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Data -> {RE_G_Variable_Name} : {RE_G_Value}")

        # Control for Reactive Energy Lagging (Single)
        else :

            # Control for Phase R Reactive Energy Lagging
            if Message.RE_G_R is not None and Message.RE_G_R > Limits.REACTIVE_ENERGY_MIN and Message.RE_G_R < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_G_R", Message.RE_G_R)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_G_R : {Message.RE_G_R}")

            # Control for Phase S Reactive Energy Lagging
            if Message.RE_G_S is not None and Message.RE_G_S > Limits.REACTIVE_ENERGY_MIN and Message.RE_G_S < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_G_S", Message.RE_G_S)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_G_S : {Message.RE_G_S}")

            # Control for Phase T Reactive Energy Lagging
            if Message.RE_G_T is not None and Message.RE_G_T > Limits.REACTIVE_ENERGY_MIN and Message.RE_G_T < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_G_T", Message.RE_G_T)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_G_T : {Message.RE_G_T}")

            # Control for Reactive Energy Lagging Average
            if Message.RE_G_A is not None and Message.RE_G_A > Limits.REACTIVE_ENERGY_MIN and Message.RE_G_A < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_G_A", Message.RE_G_A)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_G_A : {Message.RE_G_A}")

            # Control for Total Reactive Energy Lagging
            if Message.RE_G_TOT is not None and Message.RE_G_TOT > Limits.REACTIVE_ENERGY_MIN and Message.RE_G_TOT < Limits.REACTIVE_ENERGY_MAX:

                # Set ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RE_G_TOT", Message.RE_G_TOT)

                # Log Message
                Log.Terminal_Log("INFO", f"New Data -> RE_G_TOT : {Message.RE_G_TOT}")

        # Control for Frequency
        if Message.FQ is not None and Message.FQ > Limits.FREQUENCY_MIN and Message.FQ < Limits.FREQUENCY_MAX:

            # Set ST
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "FQ", Message.FQ)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> FQ : {Message.FQ}")

        # Control for MAX_TEMP Temperature
        if Message.Max78630_T is not None and Message.Max78630_T > Limits.TEMPERATURE_MIN and Message.Max78630_T < Limits.TEMPERATURE_MAX:

            # Set ST
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Max78630_T", Message.Max78630_T)

            # Log Message
            Log.Terminal_Log("INFO", f"New Data -> Max78630_T : {Message.Max78630_T}")

        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Close Database
    DB_Module.close()
