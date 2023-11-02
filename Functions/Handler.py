# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from datetime import datetime

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

# Update Device Last_Connection in Database
def Update_Device_Last_Connection(Device_ID: str):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device in Database
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Update Device Last_Connection
    Query_Device.Last_Connection = datetime.now()

    # Commit DataBase
    DB_Module.commit()

    # Close Database
    DB_Module.close()

    # Return
    return

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
def Control_Modem(IMEI: str, Firmware: str = None):

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
            Firmware = Firmware,
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

        # Control Existing Version With New Version
        if Query_Modem.Firmware != Firmware:

            # Update Modem Version
            Query_Modem.Firmware = Firmware

            # Commit DataBase
            DB_Module.commit()

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
            Operator_ID = 1,
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

# Parameter Recorder
def Parameter_Recorder(Stream_ID: int, Device_Time: datetime, Parameter: str, Value):

    # Declare Type_ID
    Type_ID = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control for Type_ID
    Query_Type_ID = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Variable.like(Parameter)).first()

    # Type_ID not in Database
    if Query_Type_ID:

        # Read Type_ID
        Type_ID = Query_Type_ID.Type_ID

    # Create New Parameter
    New_Parameter = Models.Parameter(
        Stream_ID = Stream_ID,
        Type_ID = Type_ID,
        Value = Value,
        Create_Time = Device_Time
    )
        
    # Add Record to DataBase
    DB_Module.add(New_Parameter)

    # Commit DataBase
    DB_Module.commit()

    # Refresh DataBase
    DB_Module.refresh(New_Parameter)

    # Close Database
    DB_Module.close()

# WeatherStat Recorder
def WeatherStat_Recorder(Stream_ID: int, Device_Time: datetime, Parameter: str, Value):

    # Declare Type_ID
    Type_ID = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control for Type_ID
    Query_Type_ID = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Variable.like(Parameter)).first()

    # Type_ID not in Database
    if Query_Type_ID:

        # Read Type_ID
        Type_ID = Query_Type_ID.Type_ID

    # Create New WeatherStat Measurement
    New_Measurement = Models.WeatherStat(
        Stream_ID = Stream_ID,
        Type_ID = Type_ID,
        Value = Value,
        Create_Time = Device_Time
    )
        
    # Add Record to DataBase
    DB_Module.add(New_Measurement)

    # Commit DataBase
    DB_Module.commit()

    # Refresh DataBase
    DB_Module.refresh(New_Measurement)

    # Close Database
    DB_Module.close()

