# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, View_Models, Definitions
from Functions import Log
from datetime import datetime
import math

# Control for Device in Database
def Control_Device(DB_Module, Device_ID: str):

    # Define Device Status
    Device_Status = False

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

    # Return Device Status
    return Device_Status

# Update Device Last_Connection in Database
def Update_Device_Last_Connection(DB_Module, Device_ID: str):

    # Control Device in Database
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Update Device Last_Connection
    Query_Device.Last_Connection = datetime.now()

    # Commit DataBase
    DB_Module.commit()

    # Return
    return

# Add Device to Database
def Add_Device(DB_Module, Device_ID: str, Version_ID: int, IMEI: str):

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

# Control for Version in Database
def Control_Version(DB_Module, Device_ID: str, Version: str):

    # Define Version_ID
    Version_ID = 0

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

    # Return Version_ID
    return Version_ID

# Update Device Version in Database
def Update_Version(DB_Module, Device_ID: str, Version_ID: int):

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
def Control_Modem(DB_Module, IMEI: str, Firmware: str = None):

    # Define Modem Status
    Modem_Status = False

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

    # Return Modem Status
    return Modem_Status

# Control for SIM in Database
def Control_SIM(DB_Module, ICCID: str):

    # Define SIM Status
    SIM_Status = False

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

    # Return SIM Status
    return SIM_Status

# Parameter Recorder
def Parameter_Recorder(Stream_ID: int, Device_Time: datetime, Parameter: str, Value):

    # Control for Parameter
    if Value is not None:

        # Declare Variables
        Type_ID = 0
        Type_Unit = "-"

        # Define DB
        DB_Module = Database.SessionLocal()

        # Control for Type_ID
        Query_Type_ID = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Variable.like(Parameter)).first()

        # Type_ID not in Database
        if Query_Type_ID:

            # Read Type_ID
            Type_ID = Query_Type_ID.Type_ID

            # Read Type_Unit
            Type_Unit = Query_Type_ID.Unit

            # Handle Unit
            if Type_Unit == "-" : Type_Unit = ""

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

        # Round Value
        Value = round(Value, 5)

        # Set Log Message
        Message = f"[{Parameter:^8}] - {Value:^7} {Type_Unit}"

        # Log Message
        Log.Terminal_Log("INFO", Message=Message)

# Payload Recorder
def Payload_Recorder(Stream_ID: int, Device_Time: datetime, Parameter: str, Value):

    # Control for Parameter
    if Value is not None:

        # Declare Variables
        Type_ID = 0
        Type_Unit = "-"

        # Define DB
        DB_Module = Database.SessionLocal()

        # Control for Type_ID
        Query_Type_ID = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Variable.like(Parameter)).first()

        # Type_ID not in Database
        if Query_Type_ID:

            # Read Type_ID
            Type_ID = Query_Type_ID.Type_ID

            # Read Type_Unit
            Type_Unit = Query_Type_ID.Unit

            # Handle Unit
            if Type_Unit == "-" : Type_Unit = ""

            # Create New Payload Measurement
            New_Measurement = Models.Payload(
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

        # Round Value
        Value = round(Value, 5)

        # Set Log Message
        Message = f"[{Parameter:^8}] - {Value:^7} {Type_Unit}"

        # Log Message
        Log.Terminal_Log("INFO", Message=Message)

# Get Device Last Connection Time
def Get_Device_Last_Connection(Device_ID: str):

    # Define Last_Connection
    Last_Connection = None

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Control Device in Stream Table
        Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

        # Device in Stream Table
        if Query_Device:

            # Read Stream_ID
            Last_Connection = Query_Device.Last_Connection
    
    finally:
        
        # Close Database
        DB_Module.close()

    # Return Stream_ID
    return Last_Connection

# Read Payload_Measurement
def Get_Payload_Measurement(Device_ID: str, Variable: str):

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Query Measurement at Payload_Measurement View
        Query_Measurement = DB_Module.query(View_Models.Payload_Measurement).filter(View_Models.Payload_Measurement.Device_ID == Device_ID).filter(View_Models.Payload_Measurement.Variable == Variable).first()

        # Define Measurement
        New_Measurement = Definitions.Measurement()

        # Measurement in Database
        if Query_Measurement:

            # Get Last Value
            New_Measurement.Last_Value = Query_Measurement.Value

            # Get Last Time
            New_Measurement.Last_Time = Query_Measurement.Create_Time.strftime("%Y-%m-%d %H:%M:%S")

            # Get Previous Value
            New_Measurement.Previous_Value = Query_Measurement.PreviousValue

            # Get Trend
            New_Measurement.Trend = Query_Measurement.Trend

            # Get Min Value
            New_Measurement.Min = Query_Measurement.Min

            # Get Min Time
            New_Measurement.Min_Time = Query_Measurement.Min_Time.strftime("%Y-%m-%d %H:%M:%S")

            # Get Max Value
            New_Measurement.Max = Query_Measurement.Max

            # Get Max Time
            New_Measurement.Max_Time = Query_Measurement.Max_Time.strftime("%Y-%m-%d %H:%M:%S")

        # Measurement not in Database
        else:

            # Set None
            New_Measurement = None

    finally:

        # Close Database
        DB_Module.close()

    # Return Measurement
    return New_Measurement

# AT_FL Calculator
def FL_Calculator(Temperature: float, Humidity: float):

    # Control for None
    if Temperature is not None and Humidity is not None:

        try:

            # Control for Temperature
            Temperature_F = (Temperature * 9/5) + 32

            # Constants
            c1 = -42.379
            c2 = 2.04901523
            c3 = 10.14333127
            c4 = -0.22475541
            c5 = -6.83783e-3
            c6 = -5.481717e-2
            c7 = 1.22874e-3
            c8 = 8.5282e-4
            c9 = -1.99e-6

            # AT Feel Like Calculation
            HI_fahrenheit = (c1 + (c2 * Temperature_F) + (c3 * Humidity) + (c4 * Temperature_F * Humidity) + (c5 * Temperature_F**2) + (c6 * Humidity**2) + (c7 * Temperature_F**2 * Humidity) + (c8 * Temperature_F * Humidity**2) + (c9 * Temperature_F**2 * Humidity**2))

            # Isı indeksini Fahrenheit'ten Celsius'a çevirme
            HI_celsius = (HI_fahrenheit - 32) * 5/9

            return HI_celsius

        except:

            # Return None
            return None

# Dew Point Calculator
def Dew_Calculator(Temperature: float, Humidity: float):

    # Control for None
    if Temperature is not None and Humidity is not None:

        try:

            # Constants
            a = 17.27
            b = 237.7

            # Alpha Calculation
            alpha = ((a * Temperature) / (b + Temperature)) + math.log(Humidity/100.0)
            
            # Dew Point Calculation
            dew_point = (b * alpha) / (a - alpha)

            # Return Dew Point
            return dew_point

        except:

            # Return None
            return None
