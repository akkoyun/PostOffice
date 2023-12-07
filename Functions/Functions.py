# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from datetime import timezone, timedelta, datetime
from dateutil import parser
from Functions import Log
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Get Service Status
def Get_Service_Status(Service: str):

    # Define Status
    Service_State = False

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Control Service
        Query_Status = (DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like(Service)).order_by(Models.Service_LOG.Update_Time.desc()).first())

        # Service Found
        if Query_Status is not None:

            # Return Service State
            Service_State = Query_Status.Status

    finally:
        
        # Close Database
        DB_Module.close()

    # Return Status
    return Service_State

# Control Last Update Interval
def Check_Up_to_Date(last_time: str, threshold_minutes: int = 32):

    # Convert to Datetime using dateutil.parser and set to UTC
    last_time = parser.parse(last_time).astimezone(timezone.utc)
    last_update = datetime.now(timezone.utc)

    # Calculate Difference
    time_difference = last_update - last_time
    minutes_difference = time_difference.total_seconds() / 60

    # Check if Up to Date
    return minutes_difference < threshold_minutes













# Control for Device in Database
# def Control_Device(Device_ID: str):

#     # Define Device Status
#     Device_Status = False

#     # Control for Device_ID
#     if Device_ID is not None:

#         # Define DB
#         with Database.DB_Session_Scope() as DB_Module:

#             # Query Device Project
#             Query_Device = DB_Module.query(
#                 Models.Device.Device_ID,
#                 Models.Device.Status_ID,



#                 Models.Calibration.Calibration_ID,
#                 Models.Calibration.Device_ID,
#                 Models.Data_Type.Variable,
#                 Models.Calibration.Gain,
#                 Models.Calibration.Offset,
#                 Models.Calibration.Create_Time
#             ).join(
#                 Models.Data_Type, Models.Calibration.Type_ID == Models.Data_Type.Type_ID
#             ).order_by(
#                 desc(Models.Calibration.Create_Time)
#             ).filter(Models.Calibration.Device_ID == Device_ID).filter(Models.Data_Type.Variable == Variable).first()








#             # Control Device in Database
#             Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

#             # Device not in Database
#             if Query_Device is not None:

#                 # Set Device Status
#                 Device_Status = True

#     # Return Device Status
#     return Device_Status
