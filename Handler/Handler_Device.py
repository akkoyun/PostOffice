# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka, Schema
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
def Version_Update(DB_Module, Device_ID, Message: Schema.Pack_Device):

    # Version Update
    if Message.Info.Firmware is not None and Message.Info.Hardware is not None:

        # Database Version Table Query
        Query_Version_Table = DB_Module.query(Models.Version).filter(and_(Models.Version.Device_ID.like(Device_ID), Models.Version.Version_Firmware.like(Message.Info.Firmware), Models.Version.Version_Hardware.like(Message.Info.Hardware))).first()

        # Version Not Found
        if not Query_Version_Table:

            # Create New Version
            New_Version = Models.Version(
                    Device_ID=Device_ID,
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

# Power Measurement Update Function
def Power_Update(Headers, Message: Schema.Pack_Device):

    # Add IV Measurement Record
    if Message.Power.Battery.IV is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'IV', Message.Power.Battery.IV)

    # Add AC Measurement Record
    if Message.Power.Battery.AC is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'AC', Message.Power.Battery.AC)

    # Add FB Measurement Record
    if Message.Power.Battery.FB is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'FB', Message.Power.Battery.FB)

    # Add IB Measurement Record
    if Message.Power.Battery.IB is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'IB', Message.Power.Battery.IB)

    # Add SOC Measurement Record
    if Message.Power.Battery.SOC is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'SOC', Message.Power.Battery.SOC)

    # Add T Measurement Record
    if Message.Power.Battery.T is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'T', Message.Power.Battery.T)

    # Add Charge Measurement Record
    if Message.Power.Battery.Charge is not None: Functions.Add_Device_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'Charge', Message.Power.Battery.Charge)

    # Log Message
    Log.Terminal_Log("INFO", f"Power Measurements Updated.")

# SIM Update Function
def SIM_Update(DB_Module, Message: Schema.Pack_Device):

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
        Log.Terminal_Log("INFO", f"New Connection Recorded.")

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
            Version_Update(DB_Module, Headers.Device_ID, Kafka_Device_Message)

            # Power Update
            Power_Update(Headers, Kafka_Device_Message)

            # SIM Update
            SIM_ID = SIM_Update(DB_Module, Kafka_Device_Message)




            # Connection Update
            Connection_Update(DB_Module, Headers, SIM_ID, Kafka_Device_Message.IoT.GSM.Operator.RSSI, Kafka_Device_Message.IoT.GSM.Operator.ConnTime)

            # Log to Queue
            Kafka.Send_To_Log_Topic(Headers.Device_ID, f"Connection Info Saved : {Headers.Device_IP}")










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
