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

# Control for Version in Database
def Control_Version(Version: str):

    # Define Version_ID
    Version_ID = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Version in Database
    Query_Version = DB_Module.query(Models.Version).filter(Models.Version.Firmware.like(Version)).first()

    # Version not in Database
    if not Query_Version:

        # Create New Version
        New_Version = Models.Version(
            Firmware = Version,
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
    if not Query_Device:

        # Log Message
        Log.Terminal_Log("ERROR", f"Device Not in Database : {Device_ID}")

    # Device in Database
    else:

        # Control for Version
        if Query_Device.Version_ID == Version_ID:

            # Log Message
            Log.Terminal_Log("INFO", f"Device Version is Up to Date : {Device_ID}")

        else:

            # Update Device Version
            Query_Device.Version_ID = Version_ID

            # Commit DataBase
            DB_Module.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"Device Version Updated : {Device_ID}")

    # Close Database
    DB_Module.close()

    # Return Version_ID
    return Version_ID

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


