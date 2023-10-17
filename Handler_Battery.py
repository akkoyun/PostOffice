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
            if len(Message.headers) >= 6:

                # Handle Headers
                class Headers:
                    Command = Message.headers[0][1].decode('ASCII')
                    Device_ID = Message.headers[1][1].decode('ASCII')
                    Device_Time = Message.headers[2][1].decode('ASCII')
                    Device_IP = Message.headers[3][1].decode('ASCII')
                    Size = Message.headers[4][1].decode('ASCII')
                    Stream_ID = Message.headers[5][1].decode('ASCII')

            # If not, log the error and skip to the next iteration
            else:
                
                # Log Message
                print(f"Header Error")
                
                # Skip to the next iteration
                continue

            # Variable Control

            # Set Stream ID
            Data_Stream_ID = Headers.Stream_ID

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
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
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

            # Battery AC Variable Control
            if Kafka_Power_Message.Battery.AC is not None:

                # AC Variable ID Query
                Query_Measurement_Type_AC = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('AC')).first()

                # Control for Query
                if Query_Measurement_Type_AC is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_AC = Query_Measurement_Type_AC.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_AC = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_AC,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.AC,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_AC)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_AC)

            # Battery FB Variable Control
            if Kafka_Power_Message.Battery.FB is not None:

                # FB Variable ID Query
                Query_Measurement_Type_FB = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('FB')).first()

                # Control for Query
                if Query_Measurement_Type_FB is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_FB = Query_Measurement_Type_FB.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_FB = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_FB,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.FB,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_FB)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_FB)

            # Battery IB Variable Control
            if Kafka_Power_Message.Battery.IB is not None:

                # IB Variable ID Query
                Query_Measurement_Type_IB = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('IB')).first()

                # Control for Query
                if Query_Measurement_Type_IB is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_IB = Query_Measurement_Type_IB.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_IB = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_IB,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.IB,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_IB)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_IB)

            # Battery SOC Variable Control
            if Kafka_Power_Message.Battery.SOC is not None:

                # SOC Variable ID Query
                Query_Measurement_Type_SOC = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('SOC')).first()

                # Control for Query
                if Query_Measurement_Type_SOC is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_SOC = Query_Measurement_Type_SOC.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_SOC = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_SOC,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.SOC,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_SOC)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_SOC)

            # Battery T Variable Control
            if Kafka_Power_Message.Battery.T is not None:

                # T Variable ID Query
                Query_Measurement_Type_T = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('T')).first()

                # Control for Query
                if Query_Measurement_Type_T is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_T = Query_Measurement_Type_T.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_T = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_T,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.T,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_T)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_T)

            # Battery Charge Variable Control
            if Kafka_Power_Message.Battery.Charge is not None:

                # Charge Variable ID Query
                Query_Measurement_Type_Charge = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_Variable.like('Charge')).first()

                # Control for Query
                if Query_Measurement_Type_Charge is not None:

                    # Get Measurement Type ID
                    Measurement_Type_ID_Charge = Query_Measurement_Type_Charge.Measurement_Type_ID

                    # Create New Version
                    New_Measurement_Charge = Models.Measurement(
                    	Data_Stream_ID = Data_Stream_ID,
                        Device_ID = Headers.Device_ID,
                        Measurement_Type_ID = Measurement_Type_ID_Charge,
                        Measurement_Data_Count = 1,
                        Measurement_Value = Kafka_Power_Message.Battery.Charge,
                        Measurement_Create_Date = Headers.Device_Time
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_Charge)

                    # Commit DataBase
                    DB_Module.commit()

                    # Refresh DataBase
                    DB_Module.refresh(New_Measurement_Charge)

    finally:

        # Close Database
        DB_Module.close()            

# Handle Device
Power_Handler()
