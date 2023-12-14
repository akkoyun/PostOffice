# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from Functions import Log

# Define Device
class Device:

    # Define Device
    def __init__(self, device_id = None, new_device = None, manufacturer_id = None, project_id = None, status_id = None, model_id = None, firmware = None, version_id = None, new_version = None, client_ip = None, modem_firmware = None, modem_firmware_new = None, imei = None, new_modem = None, iccid = None, new_sim = None, last_stream_id = None, last_connection_time = None):
        
        # Define Device
        self.Device_ID = device_id
        self.New_Device = new_device
        self.Manufacturer_ID = manufacturer_id
        self.Project_ID = project_id
        self.Status_ID = status_id
        self.Model_ID = model_id
        self.Firmware = firmware
        self.Version_ID = version_id
        self.New_Version = new_version
        self.Client_IP = client_ip
        self.IMEI = imei
        self.Modem_Firmware = modem_firmware
        self.Modem_Firmware_New = modem_firmware_new
        self.New_Modem = new_modem
        self.ICCID = iccid
        self.New_SIM = new_sim
        self.Last_Stream_ID = last_stream_id
        self.Last_Connection_Time = last_connection_time

# Define Headers
class Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size, body):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size
        self.Body = body

# Define Headers
class Handler_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size, stream_id, status_id, project_id):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size
        self.Stream_ID = stream_id
        self.Status_ID = status_id
        self.Project_ID = project_id

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





# Define Kafka Header
class Kafka_Header:
    
    # Define Kafka Header
    def __init__(self, header, device, stream_id):
        self.header = header
        self.device = device
        self.stream_id = stream_id

    def Get(self):
        
        # Get New Header
        new_header = [
            ("Command", bytes(self.header.Command, 'utf-8')), 
            ("Device_ID", bytes(self.header.Device_ID, 'utf-8')),
            ("Device_Time", bytes(self.header.Device_Time, 'utf-8')), 
            ("Device_IP", bytes(self.header.Device_IP, 'utf-8')),
            ("Size", bytes(self.header.Size, 'utf-8')),
            ("Stream_ID", bytes(str(self.stream_id), 'utf-8')),
            ("Status_ID", bytes(str(self.device.Status_ID), 'utf-8')),
            ("Project_ID", bytes(str(self.device.Project_ID), 'utf-8'))
        ]

        # Return New Header
        return new_header

# Get Variable List
def Variable_List(Segment: int):

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






