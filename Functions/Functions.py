# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Definitions, Schema
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







# Control Device Version
def Update_Version(Device_ID: str, Version: str):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Define Version_ID
        Version_ID = 0

        # Query Version_ID from Version
        Query_Version = DB_Module.query(Models.Version).filter(Models.Version.Device_ID.like(Device_ID)).filter(Models.Version.Firmware.like(Version)).first()

        # Version Found
        if Query_Version is not None:

            # Get Version_ID
            Version_ID = Query_Version.Version_ID
        
        # Version Not Found
        else:

            # Create New Version
            New_Version = Models.Version(
                Device_ID = Device_ID,
                Firmware = Version
            )

            # Add Version to DataBase
            DB_Module.add(New_Version)

            # Commit DataBase
            DB_Module.commit()

            # Get Version_ID
            Version_ID = New_Version.Version_ID

        # Query Device_ID from Device
        Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

        # Control for Version Up to Date
        if Query_Device.Version_ID != Version_ID:

            # Update Device Version
            Query_Device.Version_ID = Version_ID

            # Commit DataBase
            DB_Module.commit()

            # Return True
            return Query_Device.Version_ID
        
        # Version is Same
        else:

            # Return False
            return Version_ID




