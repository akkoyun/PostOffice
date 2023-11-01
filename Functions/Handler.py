# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from Functions import Log

# Control for Device in Database
def Control_Device_Table(Device_ID: str):

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
def Control_Version_Table(Version: str):

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

