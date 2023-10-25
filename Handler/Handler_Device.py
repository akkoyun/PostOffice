# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka
from datetime import datetime
from Setup import Functions as Functions
from sqlalchemy import and_

# Device Update Function
def Device_Update(DB_Module, Device_ID):

    # Database Device Table Query
    Query_Device_Table = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Device_ID)).first()

    # Device Not Found
    if not Query_Device_Table:

        # Create New Device
        New_Device = Models.Device(
                Device_ID=Device_ID,
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
        Log.Terminal_Log("INFO", f"New Device Added: {Device_ID}")

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

# Version Update Function
def Version_Update(DB_Module, Device_ID, FW, HW):

    # Database Version Table Query
    Query_Version_Table = DB_Module.query(Models.Version).filter(and_(Models.Version.Device_ID.like(Device_ID), Models.Version.Version_Firmware.like(FW), Models.Version.Version_Hardware.like(HW))).first()

    # Version Not Found
    if not Query_Version_Table:

        # Create New Version
        New_Version = Models.Version(
                Device_ID=Device_ID,
                Version_Firmware=FW,
                Version_Hardware=HW,
                Version_Update_Date=datetime.now()
        )

        # Add Record to DataBase
        DB_Module.add(New_Version)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Version)

        # Log Message
        Log.Terminal_Log("INFO", f"Device Version Updated: {Device_ID} - {FW} - {HW}")

# Power Measurement Update Function
def Power_Update(Headers, Message):

    # Add IV Measurement Record
    if Message.Power.Battery.IV is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'IV', Message.Battery.IV)

    # Add AC Measurement Record
    if Message.Power.Battery.AC is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'AC', Message.Battery.AC)

    # Add FB Measurement Record
    if Message.Power.Battery.FB is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'FB', Message.Battery.FB)

    # Add IB Measurement Record
    if Message.Power.Battery.IB is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'IB', Message.Battery.IB)

    # Add SOC Measurement Record
    if Message.Power.Battery.SOC is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'SOC', Message.Battery.SOC)

    # Add T Measurement Record
    if Message.Power.Battery.T is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'T', Message.Battery.T)

    # Add Charge Measurement Record
    if Message.Power.Battery.Charge is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'Charge', Message.Battery.Charge)

# SIM Update Function
def SIM_Update(DB_Module, ICCID, MCC, MNC):

    # Initialize SIM ID
    SIM_ID = 0

    # Query SIM Table
    Query_SIM_Table = DB_Module.query(Models.SIM).filter(Models.SIM.SIM_ICCID.like(ICCID)).first()

    # SIM Record Not Found
    if not Query_SIM_Table:

        # Create New SIM Record
        New_SIM = Models.SIM(
            SIM_ICCID = ICCID,
            MCC_ID = MCC,
            MNC_ID = MNC,
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
            Log.Terminal_Log("INFO", f"New SIM Added: {New_SIM.SIM_ID}")

            # Refresh DataBase
            DB_Module.refresh(New_SIM)

            # Set SIM ID
            SIM_ID = New_SIM.SIM_ID

        except Exception as e:

            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

            # Rollback DataBase
            DB_Module.rollback()

    # Get SIM ID
    SIM_ID = New_SIM.SIM_ID

    # Return SIM ID
    return SIM_ID

# Connection Update Function
def Connection_Update(DB_Module, Headers, SIM_ID, RSSI, ConnTime):

    # Control for RSSI
    if RSSI is None:
        RSSI = 0

    # Control for ConnTime
    if ConnTime is None:
        ConnTime = 0

    # Create New Connection Record
    New_Connection = Models.Connection(
        Device_ID = Headers.Device_ID,
        SIM_ID = SIM_ID,
        Connection_RSSI = RSSI,
        Connection_IP = Headers.Device_IP,
        Connection_Time = ConnTime,
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
        Log.Terminal_Log("INFO", f"New Connection Added: {New_Connection.Connection_ID}")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

        # Rollback DataBase
        DB_Module.rollback()

# Module Update Function
def Module_Update(DB_Module, Headers, SIM_ID, IMEI, Firmware):

    # Initialize Module Table
    Query_Module_Table = None

    # Control for Firmware
    if Firmware is not None:

        # Query Module Table
        Query_Module_Table = DB_Module.query(Models.IoT_Module).filter(and_(Models.IoT_Module.Module_IMEI.like(IMEI), Models.IoT_Module.Module_Firmware.like(Firmware))).first()
    
    # Firmware not found
    else:

        # Query Module Table
        Query_Module_Table = DB_Module.query(Models.IoT_Module).filter(Models.IoT_Module.Module_IMEI.like(IMEI)).first()

    # Module Record Not Found
    if not Query_Module_Table:

        # Create New Module Record
        New_Module = Models.IoT_Module(
            Device_ID = Headers.Device_ID,
            Module_Firmware = Firmware,
            Module_IMEI = IMEI
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
            Log.Terminal_Log("INFO", f"New Module Added: {New_Module.Module_ID}")

        # Except Error
        except Exception as e:

            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while adding Module: {e}")

            # Rollback DataBase
            DB_Module.rollback()

    # Module Record Found
    else:

        # Control for Firmware
        if Firmware != Query_Module_Table.Module_Firmware:

            # Update Module Record
            setattr(Query_Module_Table, 'Module_Firmware', (Firmware))

            # Commit DataBase
            DB_Module.commit()

            # Log Message
            Log.Terminal_Log("INFO", f"Module Firmware Updated")

# Parser Function
def Device_Handler():

    # Handle Messages
    try:

        # Define DB
        DB_Module = Database.SessionLocal()

        # Parse Messages
        for Message in Kafka.Kafka_Device_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Log Message
            Log.Terminal_Log("INFO", f"New Device Message Received : {Headers.Device_ID}")

            # Decode Message
            Kafka_Device_Message = Kafka.Decode_Device_Message(Message)

            # Device Update
            Device_Update(DB_Module, Headers.Device_ID)

            # Version Update
            if Kafka_Device_Message.Info.Firmware is not None and Kafka_Device_Message.Info.Hardware is not None:
                
                # Version Update
                Version_Update(DB_Module, Headers.Device_ID, Kafka_Device_Message.Info.Firmware, Kafka_Device_Message.Info.Hardware)

                # Log to Queue
                Kafka.Send_To_Log_Topic(Headers.Device_ID, f"Device Info Saved : {Headers.Device_IP}")








            # Log Message
            Log.Terminal_Log("INFO", f"-----------------------------------------------------------")

            # Commit Queue
            Kafka.Kafka_Device_Consumer.commit()

    finally:

        # Log Message
        Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
