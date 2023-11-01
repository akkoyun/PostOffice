# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models

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