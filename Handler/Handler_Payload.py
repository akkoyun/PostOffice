# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database
from Functions import Kafka, Log, Handler

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
        Log.Terminal_Log("INFO", f"----------  Payloads  ----------")

        # Convert Device Time (str) to datetime
        Device_Time = RAW_Headers.Device_Time.replace("T", " ").replace("Z", "")

        # Decode Message
        Message = Kafka.Decode_Payload_Message(RAW_Message)

        # Control for Location
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Latitude", Message.Latitude)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Longitude", Message.Longitude)

        # Control for PCB Initial Measurements
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PCB_T", Message.PCB_T)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PCB_H", Message.PCB_H)

        # WeatherStat Payloads
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AT", Message.AT)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AH", Message.AH)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AT_FL", Handler.FL_Calculator(Message.AT, Message.AH))
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AT_Dew", Handler.Dew_Calculator(Message.AT, Message.AH))
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AP", Message.AP)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VL", Message.VL)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IR", Message.IR)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "UV", Message.UV)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "WD", Message.WD)
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "WS", Message.WS)
        if Message.R is not None: Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "R", (Message.R / 200))
        if Message.ST is not None:

            # Loop Through Measurements
            for index, ST_Value in enumerate(Message.ST):

                # Set Dynamic Variable Name
                ST_Variable_Name = f"ST{index}"

                # Control for ST
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, ST_Variable_Name, ST_Value)
        else:

            # Control for ST
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST0", Message.ST_0)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST1", Message.ST_1)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST2", Message.ST_2)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST3", Message.ST_3)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST4", Message.ST_4)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST5", Message.ST_5)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST6", Message.ST_6)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST7", Message.ST_7)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST8", Message.ST_8)
            Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "ST9", Message.ST_9)

        # PowerStat Payloads
        if Message.V is not None:

            if Message.V is not None:

                # Loop Through Measurements
                for index, V_Value in enumerate(Message.V):

                    # Set Dynamic Variable Name
                    if index == 0: V_Variable_Name = "V_R"
                    if index == 1: V_Variable_Name = "V_S"
                    if index == 2: V_Variable_Name = "V_T"
                    if index == 3: V_Variable_Name = "V_A"

                    # Record Measurement
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, V_Variable_Name, V_Value)
            else :

                # Control for Instant Voltage
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "V_R", Message.V_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "V_S", Message.V_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "V_T", Message.V_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "V_A", Message.V_A)
        if Message.VRMS is not None:

            if Message.VRMS is not None:

                # Loop Through Measurements
                for index, VRMS_Value in enumerate(Message.VRMS):

                    # Set Dynamic Variable Name
                    if index == 0: VRMS_Variable_Name = "VRMS_R"
                    if index == 1: VRMS_Variable_Name = "VRMS_S"
                    if index == 2: VRMS_Variable_Name = "VRMS_T"
                    if index == 3: VRMS_Variable_Name = "VRMS_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, VRMS_Variable_Name, VRMS_Value)
            else :

                # Control for Phase R RMS Voltage
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VRMS_R", Message.VRMS_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VRMS_S", Message.VRMS_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VRMS_T", Message.VRMS_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VRMS_A", Message.VRMS_A)
        if Message.VFun is not None:

            if Message.VFun is not None:

                # Loop Through Measurements
                for index, VFun_Value in enumerate(Message.VFun):

                    # Set Dynamic Variable Name
                    if index == 0: VFun_Variable_Name = "VFun_R"
                    if index == 1: VFun_Variable_Name = "VFun_S"
                    if index == 2: VFun_Variable_Name = "VFun_T"
                    if index == 3: VFun_Variable_Name = "VFun_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, VFun_Variable_Name, VFun_Value)
            else :

                # Control for Phase R Fundamental Voltage
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VFun_R", Message.VFun_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VFun_S", Message.VFun_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VFun_T", Message.VFun_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VFun_A", Message.VFun_A)
        if Message.VHarm is not None:

            if Message.VHarm is not None:

                # Loop Through Measurements
                for index, VHarm_Value in enumerate(Message.VHarm):

                    # Set Dynamic Variable Name
                    if index == 0: VHarm_Variable_Name = "VHarm_R"
                    if index == 1: VHarm_Variable_Name = "VHarm_S"
                    if index == 2: VHarm_Variable_Name = "VHarm_T"
                    if index == 3: VHarm_Variable_Name = "VHarm_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, VHarm_Variable_Name, VHarm_Value)
            else :

                # Control for Phase R Harmonic Voltage
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VHarm_R", Message.VHarm_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VHarm_S", Message.VHarm_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VHarm_T", Message.VHarm_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "VHarm_A", Message.VHarm_A)
        if Message.I is not None:

            if Message.I is not None:

                # Loop Through Measurements
                for index, I_Value in enumerate(Message.I):

                    # Set Dynamic Variable Name
                    if index == 0: I_Variable_Name = f"I_R"
                    if index == 1: I_Variable_Name = f"I_S"
                    if index == 2: I_Variable_Name = f"I_T"
                    if index == 3: I_Variable_Name = f"I_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, I_Variable_Name, I_Value)
            else :

                # Control for Phase R Instant Current
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "I_R", Message.I_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "I_S", Message.I_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "I_T", Message.I_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "I_A", Message.I_A)
        if Message.IP is not None:

            if Message.IP is not None:

                # Loop Through Measurements
                for index, IP_Value in enumerate(Message.IP):

                    # Set Dynamic Variable Name
                    if index == 0: IP_Variable_Name = f"IP_R"
                    if index == 1: IP_Variable_Name = f"IP_S"
                    if index == 2: IP_Variable_Name = f"IP_T"
                    if index == 3: IP_Variable_Name = f"IP_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, IP_Variable_Name, IP_Value)
            else :

                # Control for Phase R Peak Current
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IP_R", Message.IP_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IP_S", Message.IP_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IP_T", Message.IP_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IP_A", Message.IP_A)
        if Message.IRMS is not None:

            if Message.IRMS is not None:

                # Loop Through Measurements
                for index, IRMS_Value in enumerate(Message.IRMS):

                    # Set Dynamic Variable Name
                    if index == 0: IRMS_Variable_Name = "IRMS_R"
                    if index == 1: IRMS_Variable_Name = "IRMS_S"
                    if index == 2: IRMS_Variable_Name = "IRMS_T"
                    if index == 3: IRMS_Variable_Name = "IRMS_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, IRMS_Variable_Name, IRMS_Value)
            else :

                # Control for Phase R RMS Current
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IRMS_R", Message.IRMS_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IRMS_S", Message.IRMS_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IRMS_T", Message.IRMS_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IRMS_A", Message.IRMS_A)
        if Message.IFun is not None:

            if Message.IFun is not None:

                # Loop Through Measurements
                for index, IFun_Value in enumerate(Message.IFun):

                    # Set Dynamic Variable Name
                    if index == 0: IFun_Variable_Name = "IFun_R"
                    if index == 1: IFun_Variable_Name = "IFun_S"
                    if index == 2: IFun_Variable_Name = "IFun_T"
                    if index == 3: IFun_Variable_Name = "IFun_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, IFun_Variable_Name, IFun_Value)
            else :

                # Control for Phase R Fundamental Current
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IFun_R", Message.IFun_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IFun_S", Message.IFun_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IFun_T", Message.IFun_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IFun_A", Message.IFun_A)
        if Message.IHarm is not None:

            if Message.IHarm is not None:

                # Loop Through Measurements
                for index, IHarm_Value in enumerate(Message.IHarm):

                    # Set Dynamic Variable Name
                    if index == 0: IHarm_Variable_Name = "IHarm_R"
                    if index == 1: IHarm_Variable_Name = "IHarm_S"
                    if index == 2: IHarm_Variable_Name = "IHarm_T"
                    if index == 3: IHarm_Variable_Name = "IHarm_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, IHarm_Variable_Name, IHarm_Value)
            else :

                # Control for Phase R Harmonic Current
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IHarm_R", Message.IHarm_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IHarm_S", Message.IHarm_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IHarm_T", Message.IHarm_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "IHarm_A", Message.IHarm_A)
        if Message.P is not None:

            if Message.P is not None:

                # Loop Through Measurements
                for index, P_Value in enumerate(Message.P):

                    # Set Dynamic Variable Name
                    if index == 0: P_Variable_Name = "P_R"
                    if index == 1: P_Variable_Name = "P_S"
                    if index == 2: P_Variable_Name = "P_T"
                    if index == 3: P_Variable_Name = "P_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, P_Variable_Name, P_Value)
            else :

                # Control for Phase R Active Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "P_R", Message.P_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "P_S", Message.P_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "P_T", Message.P_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "P_A", Message.P_A)
        if Message.Q is not None:

            if Message.Q is not None:

                # Loop Through Measurements
                for index, Q_Value in enumerate(Message.Q):

                    # Set Dynamic Variable Name
                    if index == 0: Q_Variable_Name = "Q_R"
                    if index == 1: Q_Variable_Name = "Q_S"
                    if index == 2: Q_Variable_Name = "Q_T"
                    if index == 3: Q_Variable_Name = "Q_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, Q_Variable_Name, Q_Value)
            else :

                # Control for Phase R Reactive Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Q_R", Message.Q_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Q_S", Message.Q_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Q_T", Message.Q_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Q_A", Message.Q_A)
        if Message.S is not None:

            if Message.S is not None:

                # Loop Through Measurements
                for index, S_Value in enumerate(Message.S):

                    # Set Dynamic Variable Name
                    if index == 0: S_Variable_Name = f"S_R"
                    if index == 1: S_Variable_Name = f"S_S"
                    if index == 2: S_Variable_Name = f"S_T"
                    if index == 3: S_Variable_Name = f"S_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, S_Variable_Name, S_Value)
            else :

                # Control for Phase R Apparent Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "S_R", Message.S_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "S_S", Message.S_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "S_T", Message.S_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "S_A", Message.S_A)
        if Message.QFun is not None:

            if Message.QFun is not None:

                # Loop Through Measurements
                for index, QFun_Value in enumerate(Message.QFun):

                    # Set Dynamic Variable Name
                    if index == 0: QFun_Variable_Name = "QFun_R"
                    if index == 1: QFun_Variable_Name = "QFun_S"
                    if index == 2: QFun_Variable_Name = "QFun_T"
                    if index == 3: QFun_Variable_Name = "QFun_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, QFun_Variable_Name, QFun_Value)
            else :

                # Control for Phase R Fundamental Reactive Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QFun_R", Message.QFun_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QFun_S", Message.QFun_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QFun_T", Message.QFun_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QFun_A", Message.QFun_A)
        if Message.QHarm is not None:

            if Message.QHarm is not None:

                # Loop Through Measurements
                for index, QHarm_Value in enumerate(Message.QHarm):

                    # Set Dynamic Variable Name
                    if index == 0: QHarm_Variable_Name = "QHarm_R"
                    if index == 1: QHarm_Variable_Name = "QHarm_S"
                    if index == 2: QHarm_Variable_Name = "QHarm_T"
                    if index == 3: QHarm_Variable_Name = "QHarm_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, QHarm_Variable_Name, QHarm_Value)
            else :

                # Control for Phase R Harmonic Reactive Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QHarm_R", Message.QHarm_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QHarm_S", Message.QHarm_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QHarm_T", Message.QHarm_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "QHarm_A", Message.QHarm_A)
        if Message.PFun is not None:

            if Message.PFun is not None:

                # Loop Through Measurements
                for index, PFun_Value in enumerate(Message.PFun):

                    # Set Dynamic Variable Name
                    if index == 0: PFun_Variable_Name = "PFun_R"
                    if index == 1: PFun_Variable_Name = "PFun_S"
                    if index == 2: PFun_Variable_Name = "PFun_T"
                    if index == 3: PFun_Variable_Name = "PFun_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PFun_Variable_Name, PFun_Value)
            else :

                # Control for Phase R Fundamental Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PFun_R", Message.PFun_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PFun_S", Message.PFun_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PFun_T", Message.PFun_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PFun_A", Message.PFun_A)
        if Message.PHarm is not None:

            if Message.PHarm is not None:

                # Loop Through Measurements
                for index, PHarm_Value in enumerate(Message.PHarm):

                    # Set Dynamic Variable Name
                    if index == 0: PHarm_Variable_Name = "PHarm_R"
                    if index == 1: PHarm_Variable_Name = "PHarm_S"
                    if index == 2: PHarm_Variable_Name = "PHarm_T"
                    if index == 3: PHarm_Variable_Name = "PHarm_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PHarm_Variable_Name, PHarm_Value)
            else :

                # Control for Phase R Harmonic Power
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PHarm_R", Message.PHarm_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PHarm_S", Message.PHarm_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PHarm_T", Message.PHarm_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PHarm_A", Message.PHarm_A)
        if Message.FunVA is not None:

            if Message.FunVA is not None:

                # Loop Through Measurements
                for index, FunVA_Value in enumerate(Message.FunVA):

                    # Set Dynamic Variable Name
                    if index == 0: FunVA_Variable_Name = "FunVA_R"
                    if index == 1: FunVA_Variable_Name = "FunVA_S"
                    if index == 2: FunVA_Variable_Name = "FunVA_T"
                    if index == 3: FunVA_Variable_Name = "FunVA_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, FunVA_Variable_Name, FunVA_Value)
            else :

                # Control for Phase R Fundamental Volt Ampere
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "FunVA_R", Message.FunVA_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "FunVA_S", Message.FunVA_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "FunVA_T", Message.FunVA_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "FunVA_A", Message.FunVA_A)
        if Message.PF is not None:

            if Message.PF is not None:

                # Loop Through Measurements
                for index, PF_Value in enumerate(Message.PF):

                    # Set Dynamic Variable Name
                    if index == 0: PF_Variable_Name = "PF_R"
                    if index == 1: PF_Variable_Name = "PF_S"
                    if index == 2: PF_Variable_Name = "PF_T"
                    if index == 3: PF_Variable_Name = "PF_A"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, PF_Variable_Name, PF_Value)
            else :

                # Control for Phase R Power Factor
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PF_R", Message.PF_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PF_S", Message.PF_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PF_T", Message.PF_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "PF_A", Message.PF_A)
        if Message.AE is not None:

            if Message.AE is not None:

                # Loop Through Measurements
                for index, AE_Value in enumerate(Message.AE):

                    # Set Dynamic Variable Name
                    if index == 0: AE_Variable_Name = "AE_R"
                    if index == 1: AE_Variable_Name = "AE_S"
                    if index == 2: AE_Variable_Name = "AE_T"
                    if index == 3: AE_Variable_Name = "AE_A"
                    if index == 4: AE_Variable_Name = "AE_TOT"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, AE_Variable_Name, AE_Value)
            else :

                # Control for Phase R Active Energy
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AE_R", Message.AE_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AE_S", Message.AE_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AE_T", Message.AE_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AE_A", Message.AE_A)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "AE_TOT", Message.AE_TOT)
        if Message.RE_L is not None:

            if Message.RE_L is not None:

                # Loop Through Measurements
                for index, RE_L_Value in enumerate(Message.RE_L):

                    # Set Dynamic Variable Name
                    if index == 0: RE_L_Variable_Name = "RE_L_R"
                    if index == 1: RE_L_Variable_Name = "RE_L_S"
                    if index == 2: RE_L_Variable_Name = "RE_L_T"
                    if index == 3: RE_L_Variable_Name = "RE_L_A"
                    if index == 4: RE_L_Variable_Name = "RE_L_TOT"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, RE_L_Variable_Name, RE_L_Value)
            else :

                # Control for Phase R Reactive Energy Leading
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_L_R", Message.RE_L_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_L_S", Message.RE_L_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_L_T", Message.RE_L_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_L_A", Message.RE_L_A)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_L_TOT", Message.RE_L_TOT)
        if Message.RE_G is not None:

            if Message.RE_G is not None:

                # Loop Through Measurements
                for index, RE_G_Value in enumerate(Message.RE_G):

                    # Set Dynamic Variable Name
                    if index == 0: RE_G_Variable_Name = "RE_G_R"
                    if index == 1: RE_G_Variable_Name = "RE_G_S"
                    if index == 2: RE_G_Variable_Name = "RE_G_T"
                    if index == 3: RE_G_Variable_Name = "RE_G_A"
                    if index == 4: RE_G_Variable_Name = "RE_G_TOT"

                    # Control for Limits
                    Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, RE_G_Variable_Name, RE_G_Value)
            else :

                # Control for Phase R Reactive Energy Lagging
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_G_R", Message.RE_G_R)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_G_S", Message.RE_G_S)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_G_T", Message.RE_G_T)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_G_A", Message.RE_G_A)
                Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "RE_G_TOT", Message.RE_G_TOT)

        # Control for Frequency
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "FQ", Message.FQ)

        # Control for MAX_TEMP Temperature
        Handler.Payload_Recorder(RAW_Headers.Stream_ID, Device_Time, "Max78630_T", Message.Max78630_T)

        # Commit Kafka Consumer
        Kafka.Payload_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"******************************")

finally:

    # Close Database
    DB_Module.close()
