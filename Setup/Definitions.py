# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models

# Define Device
class Device:

    # Define Device
    def __init__(self, Device_ID, Manufacturer_ID, Project_ID, Status_ID, Model_ID, Version_ID, Client_IP, IMEI, ICCID, Last_Stream_ID, Last_Connection_Time):
        
        # Define Device
        self.Device_ID = Device_ID
        self.Manufacturer_ID = Manufacturer_ID
        self.Project_ID = Project_ID
        self.Status_ID = Status_ID
        self.Model_ID = Model_ID
        self.Version_ID = Version_ID
        self.Client_IP = Client_IP
        self.IMEI = IMEI
        self.ICCID = ICCID
        self.Last_Stream_ID = Last_Stream_ID
        self.Last_Connection_Time = Last_Connection_Time

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

# Define Rain_Calculate Type
class Rain_Totals:

    # Define Rain_Totals
    def __init__(self, Device_ID = None, R_1 = None, R_24 = None, R_48 = None, R_168 = None):
        
        # Get Variables
        self.Device_ID = Device_ID
        self.R_1 = R_1
        self.R_24 = R_24
        self.R_48 = R_48
        self.R_168 = R_168

# Define Calibration Type
class Calibration:

    # Define Calibration
    def __init__(self, Gain = None, Offset = None):
        
        # Get Variables
        self.Gain = Gain
        self.Offset = Offset

# Type List Function
def Type_List(Segment: int):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Define Formatted Data
    # 0 - Unknown
    # 1 - Device
    # 2 - Power
    # 3 - GSM
    # 4 - Location
    # 5 - Environment
    # 6 - Water
    # 7 - Energy

    try:

        # Query all data types
        Data_Type_Query = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Segment_ID == Segment).all()

        # Control for Parameter Type
        if Segment == 1: Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 2: Formatted_Data = [(data_type.Variable, f"Message.Power.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 3: Formatted_Data = [(data_type.Variable, f"Message.IoT.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 4: Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 5: Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 6: Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]
        elif Segment == 7: Formatted_Data = [(data_type.Variable, f"Message.{data_type.Variable}") for data_type in Data_Type_Query]

    finally:
        
        # Close Database
        DB_Module.close()

    # End Function
    return Formatted_Data
