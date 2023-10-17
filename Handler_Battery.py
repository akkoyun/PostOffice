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
Kafka_Consumer = KafkaConsumer('Device.Power',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Power_Consumer",
                               auto_offset_reset='latest',
                               enable_auto_commit=True)

# Power Measurement Handler Function
def Power_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka_Consumer:

            # Decode Message
            # --------------

            # Decode Message
            Decoded_Value = Message.value.decode()

            # Parse JSON
            Parsed_Json = json.loads(Decoded_Value)

            # Check if JSON is a string
            if isinstance(Parsed_Json, str):
                Parsed_Json = json.loads(Parsed_Json)

            # Get Power Data
            Kafka_Power_Message = Schema.Pack_Power(**Parsed_Json)

            # Decode Headers
            # --------------

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

            # Instant Voltage Variable Control

            # Battery IV Variable Control
            if Kafka_Power_Message.Battery.IV is not None:

                # IV Variable ID Query
                Query_Measurement_Type_IV = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('IV')).first()

                # Control for Query
                if Query_Measurement_Type_IV is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_IV = Query_Measurement_Type_IV.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_IV = Models.Measurement(
                    	Data_Stream_ID = 1,
                        Measurement_Type_ID = Measurement_Type_ID_IV,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.IV,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_IV)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_IV)








    finally:

        # Close Database
        DB_Module.close()            

# Handle Device
Power_Handler()
