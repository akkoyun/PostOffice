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
