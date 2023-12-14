# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Definitions
from sqlalchemy import desc, func
from Functions import Log
from datetime import datetime, timedelta
import math

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

# Get Count
def Get_Count(Table: str):

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Handle Table Name
        if Table == 'Device': Table_Name = Models.Device
        elif Table == 'Data_Type': Table_Name = Models.Data_Type
        elif Table == 'Modem': Table_Name = Models.Modem
        elif Table == 'SIM': Table_Name = Models.SIM
        elif Table == 'Stream': Table_Name = Models.Stream
        elif Table == 'Parameter': Table_Name = Models.Parameter
        elif Table == 'Payload': Table_Name = Models.Payload
        else: Table_Name = None

        # Query Count
        Query_Count = DB_Module.query(Table_Name).count()

        # Get Count
        Count = Query_Count

    finally:

        # Close Database
        DB_Module.close()

    # Return Count
    return Count





# Get Device Last Connection Time
def Get_Device_Last_Connection(Device_ID: str):

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

# Read Payload_Measurement
def Get_Payload_Measurement(Device_ID: str, Variable: str):

    # Define Measurement
    New_Measurement = Definitions.Measurement()
    Calibration = Definitions.Calibration()

    # Control for Device_ID
    if Device_ID is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Module:

            # Query Measurement at Payload_Measurement View
            Query_Measurement = DB_Module.query(Models.Payload_Measurement).filter(Models.Payload_Measurement.Device_ID == Device_ID).filter(Models.Payload_Measurement.Variable == Variable).first()

            # Measurement in Database
            if Query_Measurement:

                # Get Last Time
                New_Measurement.Last_Time = Query_Measurement.Create_Time.strftime("%Y-%m-%d %H:%M:%S")

                # Get Min Time
                New_Measurement.Min_Time = Query_Measurement.Min_Time.strftime("%Y-%m-%d %H:%M:%S")

                # Get Max Time
                New_Measurement.Max_Time = Query_Measurement.Max_Time.strftime("%Y-%m-%d %H:%M:%S")

                # Get Calibration Gain and Offset
                Calibration = Get_Calibration(Device_ID, Variable)

                # Get Last Value
                New_Measurement.Last_Value = format(((Query_Measurement.Value * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Previous Value
                New_Measurement.Previous_Value = format(((Query_Measurement.PreviousValue * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Trend
                New_Measurement.Trend = Query_Measurement.Trend

                # Get Min Value
                New_Measurement.Min = format(((Query_Measurement.Min * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Max Value
                New_Measurement.Max = format(((Query_Measurement.Max * Calibration.Gain) + Calibration.Offset), ".4f")

                # Log Message
                if Calibration.Gain != 1 or Calibration.Offset != 0: Log.Terminal_Log("INFO", f"Calibration: {Variable} [{Device_ID}] [{Calibration.Gain}, {Calibration.Offset}]")

            # Measurement not in Database
            else:

                # Set None
                New_Measurement = None

    # Return Measurement
    return New_Measurement

# Read Parameter_Measurement
def Get_Parameter_Measurement(Device_ID: str, Variable: str):

    # Define Measurement
    New_Measurement = Definitions.Measurement()

    # Control for Device_ID
    if Device_ID is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Module:

            # Query Measurement at Payload_Measurement View
            Query_Measurement = DB_Module.query(Models.Parameter_Measurement).filter(Models.Parameter_Measurement.Device_ID == Device_ID).filter(Models.Parameter_Measurement.Variable == Variable).first()

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

    # Return Measurement
    return New_Measurement

# Read Rain_Totals
def Get_Rain_Totals(Device_ID: str):

    # Define Measurement
    New_Measurement = Definitions.Rain_Totals()
    Calibration = Definitions.Calibration()

    # Get Device_ID
    New_Measurement.Device_ID = Device_ID

    # Control for Device_ID
    if Device_ID is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Module:

            # Query Measurement at Payload_Measurement View
            Query_Measurement = DB_Module.query(Models.Rain_Calculate).filter(Models.Rain_Calculate.Device_ID == Device_ID).first()

            # Measurement in Database
            if Query_Measurement:

                # Get Calibration Gain and Offset
                Calibration = Get_Calibration(Device_ID, "R")

                # Get Last Value
                New_Measurement.R_1 = format(((Query_Measurement.R_1 * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Last Time
                New_Measurement.R_24 = format(((Query_Measurement.R_24 * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Previous Value
                New_Measurement.R_48 = format(((Query_Measurement.R_48 * Calibration.Gain) + Calibration.Offset), ".4f")

                # Get Trend
                New_Measurement.R_168 = format(((Query_Measurement.R_168 * Calibration.Gain) + Calibration.Offset), ".4f")

                # Log Message
                if Calibration.Gain != 1 or Calibration.Offset != 0: Log.Terminal_Log("INFO", f"Calibration: R [{Device_ID}] [{Calibration.Gain}, {Calibration.Offset}]")

            # Measurement not in Database
            else:

                # Set None
                New_Measurement = None

    # Return Measurement
    return New_Measurement

# Read Calibration
def Get_Calibration(Device_ID: str, Variable: str):

    # Define Calibration
    New_Calibration = Definitions.Calibration()

    # Set Defaults
    New_Calibration.Gain = 1
    New_Calibration.Offset = 0

    # Control for Device_ID
    if Device_ID is not None:

        # Define DB
        with Database.DB_Session_Scope() as DB_Module:

            # Query Calibration at Calibration Table
            Query_Calibration = DB_Module.query(
                Models.Calibration.Calibration_ID,
                Models.Calibration.Device_ID,
                Models.Data_Type.Variable,
                Models.Calibration.Gain,
                Models.Calibration.Offset,
                Models.Calibration.Create_Time
            ).join(
                Models.Data_Type, Models.Calibration.Type_ID == Models.Data_Type.Type_ID
            ).order_by(
                desc(Models.Calibration.Create_Time)
            ).filter(Models.Calibration.Device_ID == Device_ID).filter(Models.Data_Type.Variable == Variable).first()

            # Calibration in Database
            if Query_Calibration:

                # Get Gain
                New_Calibration.Gain = Query_Calibration.Gain

                # Get Offset
                New_Calibration.Offset = Query_Calibration.Offset

    # Return Calibration
    return New_Calibration

