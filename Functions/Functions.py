# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Definitions, Schema
from datetime import timezone, timedelta, datetime
import datetime
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







# Control for Device
def Control_Device(Device_ID: str):

    # Define DB
    with Database.DB_Session_Scope() as DB_Device:

    	# Control Device Existance
        Query_Device = DB_Device.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

        # Control Device Existance
        if Query_Device is None:

            # Create New Device
            New_Device = Models.Device(
                Device_ID = Device_ID,
                Status_ID = 1,
                Version_ID = 0,
                Model_ID = 0,
                IMEI = 0
            )

            # Add Device to DataBase
            DB_Device.add(New_Device)

            # Commit DataBase
            DB_Device.commit()

            # Refresh DataBase
            DB_Device.refresh(New_Device)

            # Log Message
            Log.Terminal_Log("INFO", f"New Device.")

        # Device Found
        else:

            # Update Device Last_Connection
            Query_Device.Last_Connection = datetime.now()

            # Commit DataBase
            DB_Device.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"Existing Device.")

# Control Device Version
def Update_Version(Device_ID: str, Firmware: str):

    # Define Version_ID
    Version_ID = 0

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query Version_ID from Version
        Query_Version = DB_Module.query(Models.Version).filter(Models.Version.Device_ID.like(Device_ID)).filter(Models.Version.Firmware.like(Firmware)).first()

        # Version Found
        if Query_Version is not None:

            # Get Version_ID
            Version_ID = Query_Version.Version_ID
        
        # Version Not Found
        else:

            # Create New Version
            New_Version = Models.Version(
                Device_ID = Device_ID,
                Firmware = Firmware
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

            # Set Version_ID
            Version_ID = Query_Device.Version_ID

        # Log Message
        Log.Terminal_Log("INFO", f"Version: {Firmware} [{Version_ID}]")

    # End Function
    return Version_ID

# Control Modem and Modem Version
def Update_Modem(Device_ID: str, IMEI: str, Firmware: str):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query IMEI from Modem
        Query_Modem = DB_Module.query(Models.Modem).filter(Models.Modem.IMEI.like(IMEI)).first()

        # Modem Not Found
        if Query_Modem is None:

            # Create New Modem
            New_Modem = Models.Modem(
                IMEI = IMEI,
                Model_ID = 0,
                Manufacturer_ID = 0,
                Firmware = Firmware
            )

            # Add Modem to DataBase
            DB_Module.add(New_Modem)

            # Commit DataBase
            DB_Module.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"Modem: {IMEI} / {Firmware} [NEW]")

        # Modem Found
        else:

            # Control for Firmware
            if Query_Modem.Firmware != Firmware:

                # Update Modem Firmware
                Query_Modem.Firmware = Firmware

                # Commit DataBase
                DB_Module.commit()

                # Log Message
                Log.Terminal_Log("INFO", f"Modem: {IMEI} / {Firmware} [Updated]")

        # Query IMEI from Device
        Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

        # Device Found
        if Query_Device is not None:

            # Update Device Modem IMEI
            Query_Device.IMEI = IMEI

            # Commit DataBase
            DB_Module.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"Modem: {IMEI} [OLD]")

# Control SIM
def Update_SIM(ICCID: str):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query ICCID from SIM
        Query_SIM = DB_Module.query(Models.SIM).filter(Models.SIM.ICCID.like(ICCID)).first()

        # SIM Not Found
        if Query_SIM is None:

            # Create New SIM
            New_SIM = Models.SIM(
                ICCID = ICCID,
                Operator_ID = 0,
                GSM_Number = 0,
                Static_IP = 0
            )

            # Add SIM to DataBase
            DB_Module.add(New_SIM)

            # Commit DataBase
            DB_Module.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"SIM: {ICCID} [NEW]")

        # SIM Found
        else:

            # Log Message
            Log.Terminal_Log("INFO", f"SIM: {ICCID} [OLD]")

# Record Stream
def Record_Stream(Device_ID: str, ICCID: str, Client_IP: str, Size: int, RAW_Data: str, Device_Time: datetime):

    # Define DB
    with Database.DB_Session_Scope() as DB_Stream:

        # Create New Stream
        New_Stream = Models.Stream(
            Device_ID = Device_ID,
            ICCID = ICCID,
            Client_IP = Client_IP,
            Size = Size,
            RAW_Data = RAW_Data,
            Device_Time = Device_Time,
            Stream_Time = datetime.now()
        )

        # Add Stream to DataBase
        DB_Stream.add(New_Stream)

        # Commit DataBase
        DB_Stream.commit()

        # Refresh DataBase
        DB_Stream.refresh(New_Stream)

        # Get Stream_ID
        Stream_ID = New_Stream.Stream_ID

        # Log Message
        Log.Terminal_Log("INFO", f"Stream Recorded: {Stream_ID}")

        # End Function
        return Stream_ID






