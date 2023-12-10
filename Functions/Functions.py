# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Definitions
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

# Get Device Information
def Device_Info(Device_ID: str):

    # Define Device
    Device = Definitions.Device()

    # Control for Device_ID
    if Device_ID is not None:

        # Set Device ID
        Device.Device_ID = Device_ID

        # Define DB
        with Database.DB_Session_Scope() as DB:

            # Query Device
            Query_Device = DB.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

            # Control for Device
            if Query_Device is not None:

                # Set Device Variables
                Device.Status_ID = Query_Device.Status_ID
                Device.Version_ID = Query_Device.Version_ID
                Device.Project_ID = Query_Device.Project_ID
                Device.Model_ID = Query_Device.Model_ID
                Device.IMEI = Query_Device.IMEI
                Device.Last_Connection_Time = Query_Device.Last_Connection

            # Query Stream
            Query_Stream = DB.query(Models.Stream).filter(Models.Stream.Device_ID.like(Device_ID)).order_by(Models.Stream.Stream_ID.desc()).first()

            # Control for Stream
            if Query_Stream is not None:

                # Set Stream Variables
                Device.Last_Stream_ID = Query_Stream.Stream_ID
                Device.ICCID = Query_Stream.ICCID
        
    # Return Device
    return Device