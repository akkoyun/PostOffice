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

# Get Device Information
def Device_Info(Header: Definitions.Headers, Data: Schema.Data_Pack):

    # Define Device
    Device = Definitions.Device()

    # Control for Device_ID
    if Data.Info.ID is not None:

        # Set Device ID
        Device.Device_ID = Data.Info.ID

        # Set Client IP
        Device.Client_IP = Header.Device_IP

        # Define DB
        with Database.DB_Session_Scope() as DB:

            # Query Device
            Query_Device = DB.query(Models.Device).filter(Models.Device.Device_ID.like(Data.Info.ID)).first()

            # Control for Device
            if Query_Device is not None:

                # Set Device Variables
                Device.New_Device = False
                Device.Status_ID = Query_Device.Status_ID
                Device.Project_ID = Query_Device.Project_ID
                Device.Model_ID = Query_Device.Model_ID
                Device.IMEI = Query_Device.IMEI
                Device.Last_Connection_Time = Query_Device.Last_Connection

                # Query Version
                Query_Version = DB.query(Models.Version).filter(Models.Version.Firmware.like(Data.Info.Firmware)).filter(Models.Version.Device_ID.like(Data.Info.ID)).first()

                # Version Found
                if Query_Version is not None:

                    # Set Version Variables
                    Device.New_Version = False

                    # Set Version ID
                    Device.Version_ID = Query_Device.Version_ID

                # Version Not Found
                else:

                    # Create New Version
                    New_Version = Models.Version(
                        Firmware = Data.Info.Firmware,
                        Device_ID = Data.Info.ID,
                    )

                    # Add Record to DataBase
                    DB.add(New_Version)

                    # Get Version ID
                    Device.Version_ID = New_Version.Version_ID

                    # Set Version Variables
                    Device.New_Version = True

                # Query Modem
                Query_Modem = DB.query(Models.Modem).filter(Models.Modem.IMEI.like(Data.Device.IoT.IMEI)).first()

                # Modem Found
                if Query_Modem is not None:

                    # Control Existing Version With New Version
                    if Query_Modem.Firmware != Data.Device.IoT.Firmware:

                        # Update Modem Version
                        Query_Modem.Firmware = Data.Device.IoT.Firmware

                        # Commit DataBase
                        DB.commit()

                    # Set Modem Variables
                    Device.New_Modem = False

                # Modem Not Found
                else:

                    # Create New Modem
                    New_Modem = Models.Modem(
                        IMEI = Data.Device.IoT.IMEI,
                        Model_ID = 0,
                        Manufacturer_ID = 0,
                        Firmware = Data.Device.IoT.Firmware,
                    )

                    # Add Record to DataBase
                    DB.add(New_Modem)

                    # Set Modem Variables
                    Device.New_Modem = True

                # Query SIM
                Query_SIM = DB.query(Models.SIM).filter(Models.SIM.ICCID.like(Data.Device.IoT.ICCID)).first()

                # SIM Found
                if Query_SIM is not None:

                    # Set SIM Variables
                    Device.New_SIM = False

                # SIM Not Found
                else:

                    # Set SIM Variables
                    Device.New_SIM = True














            # Device Not Found
            else:

                # Set Device Variables
                Device.New_Device = True

            # Query Stream
            Query_Stream = DB.query(Models.Stream).filter(Models.Stream.Device_ID.like(Device_ID)).order_by(Models.Stream.Stream_ID.desc()).first()

            # Control for Stream
            if Query_Stream is not None:

                # Set Stream Variables
                Device.Last_Stream_ID = Query_Stream.Stream_ID
                Device.ICCID = Query_Stream.ICCID
        
    # Return Device
    return Device