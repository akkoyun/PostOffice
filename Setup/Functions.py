# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Schema
import Setup.Functions as Functions
from Setup.Config import APP_Settings
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import json
from sqlalchemy import and_

# Define RAW Topic Headers
class RAW_Topic_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size

# Define Incomming Headers
class Incomming_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size

# Define Full Headers
class Full_Headers:

    # Define Incomming Headers
    def __init__(self, command, device_id, device_time, device_ip, size, data_stream_id):
        
        # Get Incomming Headers
        self.Command = command
        self.Device_ID = device_id
        self.Device_Time = device_time
        self.Device_IP = device_ip
        self.Size = size
        self.Data_Stream_ID = data_stream_id

# Handle Incomming Headers
def Handle_Headers(message):

    # Check if all required headers are present    
    if len(message.headers) >= 5:
    
        # Handle Headers
        headers = Incomming_Headers(
            message.headers[0][1].decode('ASCII'),
            message.headers[1][1].decode('ASCII'),
            message.headers[2][1].decode('ASCII'),
            message.headers[3][1].decode('ASCII'),
            message.headers[4][1].decode('ASCII')
        )

        # Return Headers
        return headers
    
    else:

        # Log Message
        Log.Device_Header_Handler_Error()

        # Skip to the next iteration
        return None

# Handle Full Headers
def Handle_Full_Headers(message):

    # Check if all required headers are present    
    if len(message.headers) >= 6:
    
        # Handle Headers
        headers = Full_Headers(
            message.headers[0][1].decode('ASCII'),
            message.headers[1][1].decode('ASCII'),
            message.headers[2][1].decode('ASCII'),
            message.headers[3][1].decode('ASCII'),
            message.headers[4][1].decode('ASCII'),
            message.headers[5][1].decode('ASCII')
        )

        # Return Headers
        return headers
    
    else:

        # Log Message
        Log.Device_Header_Handler_Error()

        # Skip to the next iteration
        return None

# Parse Headers
def Parse_Headers(Headers, Data_Stream_ID):

    try:

        # Set headers
        Kafka_Header = [
            ('Command', bytes(Headers.Command, 'utf-8')), 
            ('Device_ID', bytes(Headers.Device_ID, 'utf-8')),
            ('Device_Time', bytes(Headers.Device_Time, 'utf-8')), 
            ('Device_IP', bytes(Headers.Device_IP, 'utf-8')),
            ('Size', bytes(Headers.Size, 'utf-8')),
            ('Data_Stream_ID', bytes(Data_Stream_ID, 'utf-8'))
        ]

        # Return Kafka Header
        return Kafka_Header

    except Exception as e:

        # Log Message
        print(f"An error occurred while setting Kafka headers: {e}")
        
        # Return None
        return None

# Handle Company
def Handle_Company(Command_String):

    # Handle Company
	try:
		Company = Command_String.split(":")[0]
	except:
		Company = "Unknown"

	# End Function
	return Company

# Handle Device
def Handle_Device(Command_String):

	# Handle Device
	try:
		Device = Command_String.split(":")[1].split(".")[0]
	except:
		Device = "Unknown"

	# End Function
	return Device

# Handle Command
def Handle_Command(Command_String):

	# Handle Command
	try:
		Command = Command_String.split(":")[1].split(".")[1]
	except:
		Command = "Unknown"

	# End Function
	return Command






# Parse Headers
def Parse_RAW_Topic_Header(Command, Device_ID, Device_Time, Device_IP, Pack_Size):

    try:

        # Set headers
        RAW_Header = [
            ('Command', bytes(Command, 'utf-8')), 
            ('Device_ID', bytes(Device_ID, 'utf-8')),
            ('Device_Time', bytes(Device_Time, 'utf-8')), 
            ('Device_IP', bytes(Device_IP, 'utf-8')),
            ('Size', bytes(Pack_Size, 'utf-8')),
        ]

        # Return Kafka Header
        return RAW_Header

    except Exception as e:

        # Log Message
        print(f"An error occurred while setting RAW topic headers: {e}")
        
        # Return None
        return None












# Add Device Measurement
def Add_Device_Measurement(Headers: Full_Headers, variable_name, variable_value):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Query Measurement Type
    Query_Measurement_Type = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like(variable_name)).first()

    # Measurement Type Found
    if Query_Measurement_Type is not None:

        # Query Measurement
        New_Measurement = Models.Measurement_Device(
            Data_Stream_ID = Headers.Data_Stream_ID,
            Device_ID = Headers.Device_ID,
            Measurement_Type_ID = Query_Measurement_Type.Measurement_Type_ID,
            Measurement_Data_Count = 1,
            Measurement_Value = variable_value,
            Measurement_Create_Date = Headers.Device_Time
        )

        # Try to Add Record
        try:

            # Add Record to DataBase
            DB_Module.add(New_Measurement)

            # Commit DataBase
            DB_Module.commit()

            # Refresh DataBase
            DB_Module.refresh(New_Measurement)

        except Exception as e:

            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while adding Measurement: {e}")

            # Rollback DataBase
            DB_Module.rollback()

    # Measurement Type Not Found
    else:

        # Log Message
        Log.Terminal_Log("ERROR", f"Measurement Type '{variable_name}' not found.")

    # Close Database
    DB_Module.close()

# Add WeatherStat Measurement
def Add_WeatherStat_Measurement(Data_Stream_ID, Device_ID, Device_Time, variable_name, variable_value):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Query Measurement Type
    Query_Measurement_Type = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like(variable_name)).first()

    # Measurement Type Found
    if Query_Measurement_Type is not None:

        # Query Measurement
        New_Measurement = Models.Measurement_WeatherStat(
            Data_Stream_ID = Data_Stream_ID,
            Device_ID = Device_ID,
            Measurement_Type_ID = Query_Measurement_Type.Measurement_Type_ID,
            Measurement_Data_Count = 1,
            Measurement_Value = variable_value,
            Measurement_Create_Date = Device_Time
        )

        # Try to Add Record
        try:

            # Add Record to DataBase
            DB_Module.add(New_Measurement)

            # Commit DataBase
            DB_Module.commit()

            # Refresh DataBase
            DB_Module.refresh(New_Measurement)

            # Log Message
            Log.Terminal_Log("INFO", f"New WeatherStat Measurement {variable_name}: {variable_value} - [{New_Measurement.Measurement_ID}]")

        except Exception as e:

            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while adding Measurement: {e}")

            # Rollback DataBase
            DB_Module.rollback()

    # Measurement Type Not Found
    else:

        # Log Message
        Log.Terminal_Log("ERROR", f"Measurement Type '{variable_name}' not found.")

    # Close Database
    DB_Module.close()

# Device Handler Functions
# ------------------------

# Device Update Function
def Device_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Database Device Table Query
    Query_Device_Table = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Headers.Device_ID)).first()

    # Device Not Found
    if not Query_Device_Table:

        # Create New Device
        New_Device = Models.Device(
                Device_ID=Headers.Device_ID,
                Device_Data_Count=1,
                Device_Create_Date=datetime.now(),
                Device_Last_Online=datetime.now()
        )

        # Add Record to DataBase
        DB_Module.add(New_Device)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Device)

        # Log Message
        Log.Terminal_Log("INFO", f"New Device Added: {Headers.Device_ID}")

    # Device Found
    else:

        # Update Device
        setattr(Query_Device_Table, 'Device_Data_Count', (Query_Device_Table.Device_Data_Count + 1))

        # Update Online Time
        setattr(Query_Device_Table, 'Device_Last_Online', datetime.now())

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Device Last Online Time Updated")

    # Close Database
    DB_Module.close()

# Version Update Function
def Version_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Version Update
    if Message.Info.Firmware is not None and Message.Info.Hardware is not None:

        # Database Version Table Query
        Query_Version_Table = DB_Module.query(Models.Version).filter(and_(Models.Version.Device_ID.like(Headers.Device_ID), Models.Version.Version_Firmware.like(Message.Info.Firmware), Models.Version.Version_Hardware.like(Message.Info.Hardware))).first()

        # Version Not Found
        if not Query_Version_Table:

            # Create New Version
            New_Version = Models.Version(
                    Device_ID=Headers.Device_ID,
                    Version_Firmware=Message.Info.Firmware,
                    Version_Hardware=Message.Info.Hardware,
                    Version_Update_Date=datetime.now()
            )

            # Add Record to DataBase
            DB_Module.add(New_Version)

            # Commit DataBase
            DB_Module.commit()

            # Refresh DataBase
            DB_Module.refresh(New_Version)

            # Log Message
            Log.Terminal_Log("INFO", f"Device Version Updated: [{Message.Info.Firmware} - {Message.Info.Hardware}]")

        # Version Found
        else:

            # Log Message
            Log.Terminal_Log("INFO", f"Device Version Not Changed.")

    # Version Found
    else:

        # Log Message
        Log.Terminal_Log("WARNING", f"No Version Data on Pack.")

    # Close Database
    DB_Module.close()

# Power Measurement Update Function
def Power_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Add IV Measurement Record
    if Message.Power.Battery.IV is not None and Message.Power.Battery.IV != -9999.0 and Message.Power.Battery.IV != 9999.0:
         Add_Device_Measurement(Headers, 'IV', Message.Power.Battery.IV)

    # Add AC Measurement Record
    if Message.Power.Battery.AC is not None and Message.Power.Battery.AC != -9999.0 and Message.Power.Battery.AC != 9999.0:
         Add_Device_Measurement(Headers, 'AC', Message.Power.Battery.AC)

    # Add FB Measurement Record
    if Message.Power.Battery.FB is not None and Message.Power.Battery.FB != -9999.0 and Message.Power.Battery.FB != 9999.0:
         Add_Device_Measurement(Headers, 'FB', Message.Power.Battery.FB)

    # Add IB Measurement Record
    if Message.Power.Battery.IB is not None and Message.Power.Battery.IB != -9999.0 and Message.Power.Battery.IB != 9999.0:
         Add_Device_Measurement(Headers, 'IB', Message.Power.Battery.IB)

    # Add SOC Measurement Record
    if Message.Power.Battery.SOC is not None and Message.Power.Battery.SOC != -9999.0 and Message.Power.Battery.SOC != 9999.0:
         Add_Device_Measurement(Headers, 'SOC', Message.Power.Battery.SOC)

    # Add T Measurement Record
    if Message.Power.Battery.T is not None and Message.Power.Battery.T != -9999.0 and Message.Power.Battery.T != 9999.0:
         Add_Device_Measurement(Headers, 'T', Message.Power.Battery.T)

    # Add Charge Measurement Record
    if Message.Power.Battery.Charge is not None: 
         Add_Device_Measurement(Headers, 'Charge', Message.Power.Battery.Charge)

    # Log Message
    Log.Terminal_Log("INFO", f"Power Measurements Recorded.")

# SIM Update Function
def SIM_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Initialize SIM ID
    SIM_ID = 0

    # SIM Update
    if Message.IoT.GSM.Operator.ICCID is not None:

        # Initialize SIM Table
        New_SIM = None

        # Query SIM Table
        Query_SIM_Table = DB_Module.query(Models.SIM).filter(Models.SIM.SIM_ICCID.like(Message.IoT.GSM.Operator.ICCID)).first()

        # SIM Record Not Found
        if not Query_SIM_Table:

            # Create New SIM Record
            New_SIM = Models.SIM(
                SIM_ICCID = Message.IoT.GSM.Operator.ICCID,
                MCC_ID = Message.IoT.GSM.Operator.MCC,
                MNC_ID = Message.IoT.GSM.Operator.MNC,
                SIM_Create_Date = datetime.now()
            )

            # Add Record to DataBase
            try:

                # Add Record to DataBase
                DB_Module.add(New_SIM)

                # Database Flush
                DB_Module.flush()

                # Commit DataBase
                DB_Module.commit()

                # Log Message
                Log.Terminal_Log("INFO", f"New SIM Recorded.")

                # Refresh DataBase
                DB_Module.refresh(New_SIM)

                # Set SIM ID
                SIM_ID = New_SIM.SIM_ID

            except Exception as e:

                # Log Message
                Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

                # Rollback DataBase
                DB_Module.rollback()

        # SIM Record Found
        else:

            # Get SIM ID
            SIM_ID = Query_SIM_Table.SIM_ID

    # Close Database
    DB_Module.close()

    # Return SIM ID
    return SIM_ID

# Connection Update Function
def Connection_Update(Headers: Full_Headers, SIM_ID: int, Message: Schema.Pack_Device):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Create New Connection Record
    New_Connection = Models.Connection(
        Device_ID = Headers.Device_ID,
        SIM_ID = SIM_ID,
        Connection_RSSI = Message.IoT.GSM.Operator.RSSI,
        Connection_IP = Headers.Device_IP,
        Connection_Time = Message.IoT.GSM.Operator.ConnTime,
        Connection_Data_Size = int(Headers.Size),
        Connection_Create_Date = Headers.Device_Time
    )

    # Add Record to DataBase
    try:

        # Add Record to DataBase
        DB_Module.add(New_Connection)

        # Database Flush
        DB_Module.flush()

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Connection Recorded.")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

        # Rollback DataBase
        DB_Module.rollback()

    # Close Database
    DB_Module.close()

# Module Update Function
def Module_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Module Update
    if Message.IoT.GSM.Module.IMEI is not None:

        # Initialize Module Table
        Query_Module_Table = None

        # Control for Firmware
        if Message.IoT.GSM.Module.Firmware is not None:

            # Query Module Table
            Query_Module_Table = DB_Module.query(Models.IoT_Module).filter(and_(Models.IoT_Module.Module_IMEI.like(Message.IoT.GSM.Module.IMEI), Models.IoT_Module.Module_Firmware.like(Message.IoT.GSM.Module.Firmware))).first()

        # Firmware not found
        else:

            # Query Module Table
            Query_Module_Table = DB_Module.query(Models.IoT_Module).filter(Models.IoT_Module.Module_IMEI.like(Message.IoT.GSM.Module.IMEI)).first()

        # Module Record Not Found
        if not Query_Module_Table:

            # Create New Module Record
            New_Module = Models.IoT_Module(
                Device_ID = Headers.Device_ID,
                Module_Firmware = Message.IoT.GSM.Module.Firmware,
                Module_IMEI = Message.IoT.GSM.Module.IMEI
            )

            # Add Record to DataBase
            try:

                # Add Record to DataBase
                DB_Module.add(New_Module)

                # Database Flush
                DB_Module.flush()

                # Commit DataBase
                DB_Module.commit()

                # Log Message
                Log.Terminal_Log("INFO", f"New IoT Module Recorded.")

            # Except Error
            except Exception as e:

                # Log Message
                Log.Terminal_Log("ERROR", f"An error occurred while adding Module: {e}")

                # Rollback DataBase
                DB_Module.rollback()
    
        # Module Record Found
        else:

            # Control for Firmware
            if Message.IoT.GSM.Module.Firmware != Query_Module_Table.Module_Firmware:

                # Update Module Record
                setattr(Query_Module_Table, 'Module_Firmware', (Message.IoT.GSM.Module.Firmware))

                # Commit DataBase
                DB_Module.commit()

                # Log Message
                Log.Terminal_Log("INFO", f"IoT Module Firmware Updated")

    # Close Database
    DB_Module.close()

# Location Update Function
def Location_Update(Headers: Full_Headers, Message: Schema.Pack_Device):

    # Add TAC Measurement Record
    if Message.IoT.GSM.Operator.TAC is not None and int(Message.IoT.GSM.Operator.TAC, 16) != 0: 
        Add_Device_Measurement(Headers, 'TAC', int(Message.IoT.GSM.Operator.TAC, 16))

    # Add LAC Measurement Record
    if Message.IoT.GSM.Operator.LAC is not None and int(Message.IoT.GSM.Operator.LAC, 16) != 0:
        Add_Device_Measurement(Headers, 'LAC', int(Message.IoT.GSM.Operator.LAC, 16))

    # Add Cell_ID Measurement Record
    if Message.IoT.GSM.Operator.Cell_ID is not None and int(Message.IoT.GSM.Operator.Cell_ID, 16) != 0:
        Add_Device_Measurement(Headers, 'Cell_ID', int(Message.IoT.GSM.Operator.Cell_ID, 16))

    # Log Message
    Log.Terminal_Log("INFO", f"GSM Location Parameters Recorded.")
