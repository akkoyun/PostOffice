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











# Control for Device
def Control_Device(Device: Definitions.Device):

    # Define DB
    with Database.DB_Session_Scope() as DB_Device:

    	# Control Device Existance
        Query_Device = DB_Device.query(Models.Device).filter(Models.Device.Device_ID.like(Device.Device_ID)).first()

        # Control Device Existance
        if Query_Device is not None:

            # Update Device Last_Connection
            Query_Device.Last_Connection = datetime.now()

            # Commit DataBase
            DB_Device.commit()

            # Set Device Details
            Device.Status_ID = Query_Device.Status_ID
            Device.Version_ID = Query_Device.Version_ID
            Device.Model_ID = Query_Device.Model_ID
            Device.Project_ID = Query_Device.Project_ID
            Device.IMEI = Query_Device.IMEI
            Device.New_Device = False
            Device.Last_Connection_Time = Query_Device.Last_Connection

        # Device Found
        else:

            # Create New Device
            New_Device = Models.Device(
                Device_ID = Device.Device_ID,
                Status_ID = 1,
                Version_ID = 0,
                Model_ID = 0,
                IMEI = 0,
                Last_Connection = datetime.now(),
                Create_Time = datetime.now()
            )

            # Add Device to DataBase
            DB_Device.add(New_Device)

            # Commit DataBase
            DB_Device.commit()

            # Set Device Details
            Device.New_Device = True

    # End Function
    return Device

# Control Device Version
def Update_Version(Device: Definitions.Device):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query Version_ID from Version
        Query_Version = DB_Module.query(Models.Version).filter(Models.Version.Device_ID.like(Device.Device_ID)).filter(Models.Version.Firmware.like(Device.Firmware)).first()

        # Version Found
        if Query_Version is not None:

            # Get Version_ID
            Device.Version_ID = Query_Version.Version_ID

            # Set New Version
            Device.New_Version = False
        
        # Version Not Found
        else:

            # Create New Version
            New_Version = Models.Version(
                Device_ID = Device.Device_ID,
                Firmware = Device.Firmware,
            )

            # Add Version to DataBase
            DB_Module.add(New_Version)

            # Commit DataBase
            DB_Module.commit()

            # Refresh DataBase
            DB_Module.refresh(New_Version)

            # Get Version_ID
            Device.Version_ID = New_Version.Version_ID

            # Set New Version
            Device.New_Version = False

        # Query Device_ID from Device
        Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device.Device_ID)).first()

        # Control for Version Up to Date
        if Query_Device.Version_ID != Device.Version_ID:

            # Update Device Version
            Query_Device.Version_ID = Device.Version_ID

            # Commit DataBase
            DB_Module.commit()

            # Set Version_ID
            Device.Version_ID = Query_Device.Version_ID

            # Set New Version
            Device.New_Version = True

    # End Function
    return Device

# Control Modem and Modem Version
def Update_Modem(Device: Definitions.Device):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query IMEI from Modem
        Query_Modem = DB_Module.query(Models.Modem).filter(Models.Modem.IMEI.like(Device.IMEI)).first()

        # Modem Not Found
        if Query_Modem is None:

            # Create New Modem
            New_Modem = Models.Modem(
                IMEI = Device.IMEI,
                Model_ID = 0,
                Manufacturer_ID = 0,
                Firmware = Device.Modem_Firmware
            )

            # Add Modem to DataBase
            DB_Module.add(New_Modem)

            # Commit DataBase
            DB_Module.commit()

            # Set New Modem
            Device.New_Modem = True

        # Modem Found
        else:

            # Control for Firmware
            if Query_Modem.Firmware != Device.Modem_Firmware:

                # Update Modem Firmware
                Query_Modem.Firmware = Device.Modem_Firmware

                # Commit DataBase
                DB_Module.commit()

                # Set New Modem
                Device.New_Modem = False
                Device.Modem_Firmware_New = True

            # Modem is Up to Date
            else:

                # Set New Modem
                Device.New_Modem = False
                Device.Modem_Firmware_New = False

        # Query IMEI from Device
        Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device.Device_ID)).first()

        # Device Found
        if Query_Device is not None:

            # Control for IMEI
            if Query_Device.IMEI != Device.IMEI:

                # Update Device Modem IMEI
                Query_Device.IMEI = Device.IMEI

                # Commit DataBase
                DB_Module.commit()

# Control SIM
def Update_SIM(Device: Definitions.Device):

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Query ICCID from SIM
        Query_SIM = DB_Module.query(Models.SIM).filter(Models.SIM.ICCID.like(Device.ICCID)).first()

        # SIM Not Found
        if Query_SIM is None:

            # Create New SIM
            New_SIM = Models.SIM(
                ICCID = Device.ICCID,
                Operator_ID = 0,
                GSM_Number = 0,
                Static_IP = 0
            )

            # Add SIM to DataBase
            DB_Module.add(New_SIM)

            # Commit DataBase
            DB_Module.commit()

            # Set New SIM
            Device.New_SIM = True

        # SIM Found
        else:

            # Set New SIM
            Device.New_SIM = False

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

# Get Last Connection Time
def Get_Last_Connection(Device_ID: str):

    # Define Last_Connection
    Last_Connection = None

    # Control for Device_ID
    if Device_ID is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Module:

            # Control Device in Stream Table
            Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

            # Device in Stream Table
            if Query_Device:

                # Read Stream_ID
                Last_Connection = Query_Device.Last_Connection
        
    # Return Stream_ID
    return Last_Connection








# Measurement Recorder
def Measurement_Recorder(Measurement_Pack: Definitions.Measurement_Class):

    # Control for Parameter
    if Measurement_Pack.Value is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Measurement:

                # Create New Payload Measurement
                New_Measurement = Models.Payload(
                    Stream_ID = Measurement_Pack.Stream_ID,
                    Type_ID = Measurement_Pack.Type_ID,
                    Value = Measurement_Pack.Value,
                    Create_Time = Measurement_Pack.Device_Time
                )

                # Add Record to DataBase
                DB_Measurement.add(New_Measurement)

                # Commit DataBase
                DB_Measurement.commit()

                # Refresh DataBase
                DB_Measurement.refresh(New_Measurement)

        # Set Log Message
        Message = f"[{Measurement_Pack.Variable:^8}] - {round(Measurement_Pack.Value, 5):^7} {Measurement_Pack.Unit} [{New_Measurement.Measurement_ID}]"

        # Log Message
        Log.Terminal_Log("INFO", Message = Message)





