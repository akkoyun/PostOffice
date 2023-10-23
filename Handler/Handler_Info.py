# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka
from datetime import datetime
from Setup import Functions as Functions
from sqlalchemy import and_

# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka.Kafka_Info_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Log Message
            Log.LOG_Message(f"Message Received : {Headers.Device_ID}")

            # Decode Message
            Kafka_Info_Message = Kafka.Decode_Info_Message(Message)

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
                Log.Terminal_Log("INFO", f"Device Login Time Updated")

            # Get Consumer Record
            Firmware = Kafka_Info_Message.Firmware
            Hardware = Kafka_Info_Message.Hardware
            
            # Database Version Table Query
            Query_Version_Table = DB_Module.query(Models.Version).filter(
                and_(
                    Models.Version.Device_ID.like(Headers.Device_ID),
                    Models.Version.Version_Firmware.like(Firmware),
                    Models.Version.Version_Hardware.like(Hardware)
                )
                ).first()

            # Version Not Found
            if not Query_Version_Table:

                # Create New Version
                New_Version = Models.Version(
                        Device_ID=Headers.Device_ID,
                        Version_Firmware=Firmware,
                        Version_Hardware=Hardware,
                        Version_Update_Date=datetime.now()
                )

                # Add Record to DataBase
                DB_Module.add(New_Version)

                # Commit DataBase
                DB_Module.commit()

                # Refresh DataBase
                DB_Module.refresh(New_Version)

                # Log Message
                Log.Terminal_Log("INFO", f"New Version Added: {Headers.Device_ID} - {Firmware} - {Hardware}")

            # Version Found
            else:

                # Log Message
                Log.Terminal_Log("INFO", f"Existing Version: {Headers.Device_ID} - {Firmware} - {Hardware}")

            # Commit Queue
            Kafka.Kafka_Info_Consumer.commit()

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
