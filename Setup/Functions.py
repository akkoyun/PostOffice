# Library Includes
from Setup import Database, Models, Log, Schema
import Setup.Functions as Functions
from Setup.Config import APP_Settings
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import json

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












# Add Measurement
def Add_Measurement(Data_Stream_ID, Device_ID, Device_Time, variable_name, variable_value):

    # Define DB
    DB_Module = Database.SessionLocal()

    # Query Measurement Type
    Query_Measurement_Type = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like(variable_name)).first()

    # Measurement Type Found
    if Query_Measurement_Type is not None:

        # Query Measurement
        New_Measurement = Models.Measurement(
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
            Log.Terminal_Log("INFO", f"New Measurement {variable_name}: {variable_value} - [{New_Measurement.Measurement_ID}]")

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
