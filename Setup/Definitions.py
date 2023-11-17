# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, View_Models, Definitions
from Functions import Log
from datetime import datetime
import math

# Define Headers
class Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size

# Define Headers
class Handler_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size, stream_id):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size
        self.Stream_ID = stream_id

# Define Measurement Type
class Measurement:

    # Define Measurement
    def __init__(self, Last = None, Last_Time = None, Previous_Value = None, Trend = None, Min = None, Max = None, Min_Time = None, Max_Time = None):
        
        # Get Variables
        self.Last_Value = Last
        self.Last_Time = Last_Time
        self.Previous_Value = Previous_Value
        self.Trend = Trend
        self.Min = Min
        self.Min_Time = Min_Time
        self.Max = Max
        self.Max_Time = Max_Time

# Define Non Device Parameters
Non_Device_Parameter = [

    # Location Parameters
    ("Latitude", "Message.Latitude"),
    ("Longitude", "Message.Longitude"),

    # PCB Initial Measurements
    ("PCB_T", "Message.PCB_T"),
    ("PCB_H", "Message.PCB_H")

]

# Define WeatherStat Payload
WeatherStat_Payload = [

    # Temperature Parameters
    ("AT", "Message.AT"),
    ("AT_FL", "Handler.FL_Calculator(Message.AT, Message.AH)"),
    ("AT_Dew", "Handler.Dew_Calculator(Message.AT, Message.AH)"),

    # Humidity Parameters
    ("AH", "Message.AH"),

    # Pressure Parameters
    ("AP", "Message.AP"),
    
    # Light Parameters
    ("VL", "Message.VL"),
    ("IR", "Message.IR"),
    ("UV", "Message.UV"),
    
    # Wind Parameters
    ("WD", "Message.WD"),
    ("WS", "Message.WS"),
    
    # Rain Parameters
    ("R", "Message.R"),
    
    # Soil Temperature Parameters
    ("ST0", "Message.ST_0"),
    ("ST1", "Message.ST_1"),
    ("ST2", "Message.ST_2"),
    ("ST3", "Message.ST_3"),
    ("ST4", "Message.ST_4"),
    ("ST5", "Message.ST_5"),
    ("ST6", "Message.ST_6"),
    ("ST7", "Message.ST_7"),
    ("ST8", "Message.ST_8"),
    ("ST9", "Message.ST_9"),

]

# Define PowerStat Payload
PowerStat_Payload = [

    # Instant Voltage Parameters
    ("V_R", "Message.V_R"),
    ("V_S", "Message.V_S"),
    ("V_T", "Message.V_T"),
    ("V_A", "Message.V_A"),

    # RMS Voltage Parameters
    ("VRMS_R", "Message.VRMS_R"),
    ("VRMS_S", "Message.VRMS_S"),
    ("VRMS_T", "Message.VRMS_T"),
    ("VRMS_A", "Message.VRMS_A"),

    # Fundamental Voltage Parameters
    ("VFun_R", "Message.VFun_R"),
    ("VFun_S", "Message.VFun_S"),
    ("VFun_T", "Message.VFun_T"),
    ("VFun_A", "Message.VFun_A"),

    # Harmonic Voltage Parameters
    ("VHarm_R", "Message.VHarm_R"),
    ("VHarm_S", "Message.VHarm_S"),
    ("VHarm_T", "Message.VHarm_T"),
    ("VHarm_A", "Message.VHarm_A"),

    # Instant Current Parameters
    ("I_R", "Message.I_R"),
    ("I_S", "Message.I_S"),
    ("I_T", "Message.I_T"),
    ("I_A", "Message.I_A"),

    # Peak Current Parameters
    ("IP_R", "Message.IP_R"),
    ("IP_S", "Message.IP_S"),
    ("IP_T", "Message.IP_T"),
    ("IP_A", "Message.IP_A"),

    # RMS Current Parameters
    ("IRMS_R", "Message.IRMS_R"),
    ("IRMS_S", "Message.IRMS_S"),
    ("IRMS_T", "Message.IRMS_T"),
    ("IRMS_A", "Message.IRMS_A"),

    # Fundamental Current Parameters
    ("IFun_R", "Message.IFun_R"),
    ("IFun_S", "Message.IFun_S"),
    ("IFun_T", "Message.IFun_T"),
    ("IFun_A", "Message.IFun_A"),

    # Harmonic Current Parameters
    ("IHarm_R", "Message.IHarm_R"),
    ("IHarm_S", "Message.IHarm_S"),
    ("IHarm_T", "Message.IHarm_T"),
    ("IHarm_A", "Message.IHarm_A"),

    # Active Power Parameters
    ("P_R", "Message.P_R"),
    ("P_S", "Message.P_S"),
    ("P_T", "Message.P_T"),
    ("P_A", "Message.P_A"),

    # Reactive Power Parameters
    ("Q_R", "Message.Q_R"),
    ("Q_S", "Message.Q_S"),
    ("Q_T", "Message.Q_T"),
    ("Q_A", "Message.Q_A"),

    # Apparent Power Parameters
    ("S_R", "Message.S_R"),
    ("S_S", "Message.S_S"),
    ("S_T", "Message.S_T"),
    ("S_A", "Message.S_A"),

    # Fundamental Reactive Power Parameters
    ("QFun_R", "Message.QFun_R"),
    ("QFun_S", "Message.QFun_S"),
    ("QFun_T", "Message.QFun_T"),
    ("QFun_A", "Message.QFun_A"),

    # Harmonic Reactive Power Parameters
    ("QHarm_R", "Message.QHarm_R"),
    ("QHarm_S", "Message.QHarm_S"),
    ("QHarm_T", "Message.QHarm_T"),
    ("QHarm_A", "Message.QHarm_A"),

    # Fundamental Active Power Parameters
    ("PFun_R", "Message.PFun_R"),
    ("PFun_S", "Message.PFun_S"),
    ("PFun_T", "Message.PFun_T"),
    ("PFun_A", "Message.PFun_A"),

    # Harmonic Active Power Parameters
    ("PHarm_R", "Message.PHarm_R"),
    ("PHarm_S", "Message.PHarm_S"),
    ("PHarm_T", "Message.PHarm_T"),
    ("PHarm_A", "Message.PHarm_A"),

    # Fundamental Volt Amper Parameters
    ("FunVA_R", "Message.FunVA_R"),
    ("FunVA_S", "Message.FunVA_S"),
    ("FunVA_T", "Message.FunVA_T"),
    ("FunVA_A", "Message.FunVA_A"),

    # Power Factor Parameters
    ("PF_R", "Message.PF_R"),
    ("PF_S", "Message.PF_S"),
    ("PF_T", "Message.PF_T"),
    ("PF_A", "Message.PF_A"),

    # Active Energy Parameters
    ("AE_R", "Message.AE_R"),
    ("AE_S", "Message.AE_S"),
    ("AE_T", "Message.AE_T"),
    ("AE_A", "Message.AE_A"),
    ("AE_TOT", "Message.AE_TOT"),

    # Leading Reactive Energy Parameters
    ("RE_L_R", "Message.RE_L_R"),
    ("RE_L_S", "Message.RE_L_S"),
    ("RE_L_T", "Message.RE_L_T"),
    ("RE_L_A", "Message.RE_L_A"),
    ("RE_L_TOT", "Message.RE_L_TOT"),

    # Lagging Reactive Energy Parameters
    ("RE_G_R", "Message.RE_G_R"),
    ("RE_G_S", "Message.RE_G_S"),
    ("RE_G_T", "Message.RE_G_T"),
    ("RE_G_A", "Message.RE_G_A"),
    ("RE_G_TOT", "Message.RE_G_TOT"),

    # Frequency Parameters
    ("FQ", "Message.FQ"),

    # MAX78630 Temperature Parameters
    ("Max78630_T", "Message.Max78630_T"),

]

# Type List Function
def Type_List(Type_ID: int):

    # Define Type List
    Type_Min = Type_ID
    Type_Max = Type_ID + 1000

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Query all data types where Type_ID is >= 6000 and < 7000
        Data_Type_Query = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Type_ID >= Type_Min).filter(Models.Data_Type.Type_ID < Type_Max).all()

        # Convert query results to the specified format
        Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]

    finally:
        
        # Close Database
        DB_Module.close()

    # End Function
    return Formatted_Data
