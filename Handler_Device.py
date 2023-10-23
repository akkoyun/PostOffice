# Library Includes
from Setup import Database, Models, Log, Schema, Kafka
import json
from datetime import datetime
from sqlalchemy import and_

# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        for Message in Kafka.Kafka_Info_Consumer:

            # Log Message
            Log.LOG_Message(f"Message Received")

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

                # Log Message
                Log.LOG_Message(f"New Device Added: {Headers.Device_ID}")

            # Device Found
            else:

                # Update Device
                setattr(Query_Device_Table, 'Device_Data_Count', (Query_Device_Table.Device_Data_Count + 1))

                # Update Online Time
                setattr(Query_Device_Table, 'Device_Last_Online', datetime.now())

                # Commit DataBase
                DB_Module.commit()

                # Log Message
                Log.LOG_Message(f"Device Updated: {Headers.Device_ID}")

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
                        Version_Hardware=Hardware
                )

                # Add Record to DataBase
                DB_Module.add(New_Version)

                # Commit DataBase
                DB_Module.commit()

                # Refresh DataBase
                DB_Module.refresh(New_Version)

                # Log Message
                Log.LOG_Message(f"New Version Added: {Headers.Device_ID} - {Firmware} - {Hardware}")

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

                # Log Message
                Log.LOG_Message(f"Version Updated: {Headers.Device_ID} - {Firmware} - {Hardware}")

            # Commit Queue
            Kafka.Kafka_Info_Consumer.commit()

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
