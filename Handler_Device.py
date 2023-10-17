# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json
from datetime import datetime
from sqlalchemy import and_

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('Device.Info',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Device_Consumer",
                               auto_offset_reset='latest',
                               enable_auto_commit=True)

# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:
        for Message in Kafka_Consumer:

            # Decode Message
            decoded_value = Message.value.decode()

            # Parse JSON
            parsed_json = json.loads(decoded_value)

            # Check if JSON is a string
            if isinstance(parsed_json, str):
                parsed_json = json.loads(parsed_json)

            # Get RAW Data
            Kafka_Device_Message = Schema.Pack_Info(**parsed_json)

            # Check if all required headers are present
            if len(Message.headers) >= 6:

                # Handle Headers
                class Headers:
                    Command = Message.headers[0][1].decode('ASCII')
                    Device_ID = Message.headers[1][1].decode('ASCII')
                    Device_Time = Message.headers[2][1].decode('ASCII')
                    Device_IP = Message.headers[3][1].decode('ASCII')
                    Size = Message.headers[4][1].decode('ASCII')
                    Data_Stream_ID = Message.headers[5][1].decode('ASCII')

            # If not, log the error and skip to the next iteration
            else:
                
                # Log Message
                print(f"Header Error")
                
                # Skip to the next iteration
                continue

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

                # Get New Device ID
                Module_ID = getattr(New_Device, "Device_ID", None)

            # Device Found
            else:

                # Get Device ID
                Module_ID = getattr(Query_Device_Table, "Device_ID", None)

                # Update Device
                setattr(Query_Device_Table, 'Device_Last_Online', datetime.now())

                # Update Device
                setattr(Query_Device_Table, 'Device_Data_Count', (Query_Device_Table.Device_Data_Count + 1))

                # Commit DataBase
                DB_Module.commit()

            # Get Consumer Record
            Firmware = Kafka_Device_Message.Firmware
            Hardware = Kafka_Device_Message.Hardware

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

            # Version Found
            else:

                # Update Version
                setattr(Query_Version_Table, 'Version_Firmware', Firmware)

                # Update Version
                setattr(Query_Version_Table, 'Version_Hardware', Hardware)

                # Update Version
                setattr(Query_Version_Table, 'Version_Update_Date', datetime.now())

                # Commit DataBase
                DB_Module.commit()

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
