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

# Define Parameter Type
Parameter = [

    # Battery Parameters
    ("B_IV", "Message.Power.B_IV"),
    ("B_AC", "Message.Power.B_AC"),
    ("B_FC", "Message.Power.B_FC"),
    ("B_IC", "Message.Power.B_IC"),
    ("B_SOC", "Message.Power.B_SOC"),
    ("B_T", "Message.Power.B_T"),
    ("B_CS", "Message.Power.B_CS"),
    
    # IoT Parameters
    ("RSSI", "Message.IoT.RSSI"),
    ("ConnTime", "Message.IoT.ConnTime"),
    ("TAC", "Message.IoT.TAC"),
    ("LAC", "Message.IoT.LAC"),
    ("Cell_ID", "Message.IoT.Cell_ID")
]

# Define Non Device Parameters
Non_Device_Parameter = [

    # Location Parameters
    ("Latitude", "Message.Latitude"),
    ("Longitude", "Message.Longitude"),

    # PCB Initial Measurements
    ("PCB_T", "Message.PCB_T"),
    ("PCB_H", "Message.PCB_H")

]

# Define Weather Payload
WeatherStat_Payload = [

    # Weather Parameters
    ("AT", "Message.AT"),
    ("AH", "Message.AH"),
    ("AT_FL", "Handler.FL_Calculator(Message.AT, Message.AH)"),
    ("AT_Dew", "Handler.Dew_Calculator(Message.AT, Message.AH)"),
    ("AP", "Message.AP"),
    ("VL", "Message.VL"),
    ("IR", "Message.IR"),
    ("UV", "Message.UV"),
    ("WD", "Message.WD"),
    ("WS", "Message.WS"),
    ("R", "Message.R")

]
