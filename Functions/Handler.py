# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from Functions import Log

# Control for Device in Database
def Control_Device(Device_ID: str):

    # Define Device Status
    Device_Status = False

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device in Database
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Device not in Database
    if not Query_Device:

        # Set Device Status
        Device_Status = False

    # Device in Database
    else:

        # Set Device Status
        Device_Status = True

    # Close Database
    DB_Module.close()

    # Return Device Status
    return Device_Status

# Add Device to Database
def Add_Device(Device_ID: str, Version_ID: int, IMEI: str):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device From Table
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Device not in Database
    if not Query_Device:

        # Create New Device
        New_Device = Models.Device(
            Device_ID = Device_ID,
            Status_ID = 0,
            Version_ID = Version_ID,
            Model_ID = 0,
            IMEI = IMEI
        )

        # Add Record to DataBase
        DB_Module.add(New_Device)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Device)

    # Close Database
    DB_Module.close()

# Control for Version in Database
def Control_Version(Device_ID: str, Version: str):

    # Define Version_ID
    Version_ID = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Version in Database
    Query_Version = DB_Module.query(Models.Version).filter(Models.Version.Firmware.like(Version)).filter(Models.Version.Device_ID.like(Device_ID)).first()

    # Version not in Database
    if not Query_Version:

        # Create New Version
        New_Version = Models.Version(
            Firmware = Version,
            Device_ID = Device_ID
        )

        # Add Record to DataBase
        DB_Module.add(New_Version)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Version)

        # Get Version ID
        Version_ID = New_Version.Version_ID

    # Version in Database
    else:

        # Read Version_ID
        Version_ID = Query_Version.Version_ID

    # Close Database
    DB_Module.close()

    # Return Version_ID
    return Version_ID

# Update Device Version in Database
def Update_Version(Device_ID: str, Version_ID: int):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Version at Device Table
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Device not in Database
    if Query_Device:

        # Control for Version
        if Query_Device.Version_ID != Version_ID:

            # Update Device Version
            Query_Device.Version_ID = Version_ID

            # Commit DataBase
            DB_Module.commit()

    # Close Database
    DB_Module.close()

# Control for Modem in Database
def Control_Modem(IMEI: str):

    # Define Modem Status
    Modem_Status = False

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Modem in Database
    Query_Modem = DB_Module.query(Models.Modem).filter(Models.Modem.IMEI.like(IMEI)).first()

    # Version not in Database
    if not Query_Modem:

        # Create New Modem
        New_Modem = Models.Modem(
            IMEI = IMEI,
            Model_ID = 0,
            Manufacturer_ID = 0,
            Firmware = None,
        )

        # Add Record to DataBase
        DB_Module.add(New_Modem)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Modem)

        # Set Modem Status
        Modem_Status = True

    # Version in Database
    else:

        # Set Modem Status
        Modem_Status = False

    # Close Database
    DB_Module.close()

    # Return Modem Status
    return Modem_Status

# Control for SIM in Database
def Control_SIM(ICCID: str):

    # Define SIM Status
    SIM_Status = False

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control SIM in Database
    Query_SIM = DB_Module.query(Models.SIM).filter(Models.SIM.ICCID.like(ICCID)).first()

    # Version not in Database
    if not Query_SIM:

        # Create New SIM
        New_SIM = Models.SIM(
            ICCID = ICCID,
            Operator_ID = 0,
            GSM_Number = None,
            Static_IP = None
        )

        # Add Record to DataBase
        DB_Module.add(New_SIM)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_SIM)

        # Set SIM Status
        SIM_Status = True

    # Version in Database
    else:

        # Set Modem Status
        SIM_Status = False

    # Close Database
    DB_Module.close()

    # Return SIM Status
    return SIM_Status

