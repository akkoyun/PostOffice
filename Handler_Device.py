# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json
from datetime import datetime

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Device_Consumer",
                               auto_offset_reset='earliest',
                               enable_auto_commit=False)

# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:
        for Message in Kafka_Consumer:

            # Check if all required headers are present
            if len(Message.headers) >= 5:

                # Handle Headers
                class Headers:
                    Command = Message.headers[0][1].decode('ASCII')
                    Device_ID = Message.headers[1][1].decode('ASCII')
                    Device_Time = Message.headers[2][1].decode('ASCII')
                    Device_IP = Message.headers[3][1].decode('ASCII')
                    Size = Message.headers[4][1].decode('ASCII')

            # If not, log the error and skip to the next iteration
            else:
                
                # Log Message
                print(f"Header Error")
                
                # Skip to the next iteration
                continue

            # Database Query
            Query_Module = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Headers.Device_ID)).first()

            # Device Not Found
            if not Query_Module:

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

                # Print Device ID
                print(Module_ID)

            # Device Found
            else:

                # Get Device ID
                Module_ID = getattr(Query_Module, "Device_ID", None)

                # Update Device
                setattr(Query_Module, 'Device_Last_Online', datetime.now())

                # Update Device
                setattr(Query_Module, 'Device_Data_Count', (Query_Module.Device_Data_Count + 1))

                # Commit DataBase
                DB_Module.commit()

                # Print Device ID
                print(Module_ID)

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
