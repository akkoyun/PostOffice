# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import math

# Define Measurement Type
class Measurement:

    # Define Measurement
    def __init__(self, variable = None, last = None, change = None):
        
        # Get Variables
        self.Variable = variable
        self.Last_Value = last
        self.Change = change

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

# Get Last Stream ID
def Get_Last_Stream_ID(Device_ID: str):

    # Define Stream_ID
    Stream_ID = None

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device in Stream Table
    Query_Stream = DB_Module.query(Models.Stream).filter(Models.Stream.Device_ID.like(Device_ID)).order_by(Models.Stream.Stream_ID.desc()).first()

    # Device in Stream Table
    if Query_Stream:

        # Read Stream_ID
        Stream_ID = Query_Stream.Stream_ID

    # Close Database
    DB_Module.close()

    # Return Stream_ID
    return Stream_ID

# Get Device Last Connection Time
def Get_Device_Last_Connection(Device_ID: str):

    # Define Last_Connection
    Last_Connection = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device in Stream Table
    Query_Device = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Device in Stream Table
    if Query_Device:

        # Read Stream_ID
        Last_Connection = Query_Device.Last_Connection

    # Close Database
    DB_Module.close()

    # Return Stream_ID
    return Last_Connection

# Get Last Data on WeatherStat
def Get_WeatherStat_Data(Stream_ID: int, Variable_ID: int):

    # Define Value
    Value = None

    # Define DB
    DB_Module = Database.SessionLocal()

    # Control Device in Stream Table
    Query_Data = DB_Module.query(Models.WeatherStat).filter(Models.WeatherStat.Stream_ID == Stream_ID).filter(Models.WeatherStat.Type_ID == Variable_ID).order_by(Models.WeatherStat.Create_Time.desc()).first()

    # Device in Stream Table
    if Query_Data:

        # Read Stream_ID
        Value = Query_Data.Value

    # Close Database
    DB_Module.close()

    # Return Stream_ID
    return Value

# Get Device Last Connection Time
def Get_WeatherStat_Data_Max(Device_ID: str, Variable_Name: str = None):

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Get Max Value
        Max_Value_Query = (
            DB_Module.query(
                Models.WeatherStat.Value, 
                Models.WeatherStat.Create_Time
            )
            .join(Models.Data_Type, Models.WeatherStat.Type_ID == Models.Data_Type.Type_ID)
            .join(Models.Stream, Models.WeatherStat.Stream_ID == Models.Stream.Stream_ID)
            .filter(Models.Data_Type.Variable.like(Device_ID))
            .filter(Models.Stream.Device_ID.like(Variable_Name))
            .filter(Models.WeatherStat.Create_Time >= func.now() - func.interval('24 HOURS'))
            .order_by(Models.WeatherStat.Value.desc())
            .limit(1)
        )

        # Execute the query
        Max_Value = Max_Value_Query.one_or_none()
  
    finally:

        # Close Database
        DB_Module.close()

    # Return Value
    return Max_Value

# Get Measurement
def Read_Measurement(Device_ID: str, Variable_Name: str = None):

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # SQL Query
        Latest_Stream_Subquery = (
            DB_Module.query(Models.Stream.Stream_ID)
            .filter(Models.Stream.Device_ID == Device_ID)
            .order_by(Models.Stream.Stream_Time.desc())
            .limit(2)
            .subquery()
        )
        Target_Data_Type_Subquery = (
            DB_Module.query(Models.Data_Type.Type_ID)
            .filter(Models.Data_Type.Variable == Variable_Name)
            .subquery()
        )
        Value_Query = (
            DB_Module.query(Models.WeatherStat.Value, Models.WeatherStat.Create_Time)
            .join(Latest_Stream_Subquery, Models.WeatherStat.Stream_ID == Latest_Stream_Subquery.c.Stream_ID)
            .join(Target_Data_Type_Subquery, Models.WeatherStat.Type_ID == Target_Data_Type_Subquery.c.Type_ID)
            .order_by(Models.WeatherStat.Create_Time.desc())
            .limit(2)
        )

        # Define Measurement
        New_Measurement = Measurement()

        # Measurement in Database
        if Value_Query:

            # Set Variable Name
            New_Measurement.Variable = Variable_Name

            # Read Measurement
            New_Measurement.Last_Value = Value_Query[0].Value

            # Control for Change
            if Value_Query[0] > Value_Query[1]: New_Measurement.Change = 1
            elif Value_Query[0] < Value_Query[1]: New_Measurement.Change = -1
            else: New_Measurement.Change = 0

    except:

        # Close Database
        DB_Module.close()

        # End Function
        return None

    finally:

        # Close Database
        DB_Module.close()

    # Return Stream_ID
    return New_Measurement

# AT_FL Calculator
def FL_Calculator(Temperature: float, Humidity: float):

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
