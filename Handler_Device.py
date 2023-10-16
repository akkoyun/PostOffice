# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json
import numpy as np
from datetime import datetime

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine) 

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('RAW',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="Device_Consumer",
                               auto_offset_reset='earliest',
                               enable_auto_commit=False)

# List Finder Function
def List_Finder(List, Variable):
    for X in np.array(list(List.__dict__.items())):
        if X[0] == Variable:
            return X[1]

# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    try:
        for Message in Kafka_Consumer:

            # Handle Message
            Kafka_Message = Schema.Data_Pack_Model(**json.loads(Message.value.decode()))

            # Handle Headers
            class Headers:
                Command = Message.headers[0][1].decode('ASCII')
                Device_ID = Message.headers[1][1].decode('ASCII')
                Device_Time = Message.headers[2][1].decode('ASCII')
                Device_IP = Message.headers[3][1].decode('ASCII')
                Size = Message.headers[4][1].decode('ASCII')

            # Database Query
            Query_Module = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(Headers.Device_ID)).first()

            # Log Message
            try:
                Log.Device_Handler_Log(Headers.Device_ID)
            except Exception as e:
                Log.error(f"Logging failed: {e}")

            if not Query_Module:
                New_Module = Models.Module(
                        Device_ID=Kafka_Message.Device_ID,
                        Device_Data_Count=1,
                        Device_Create_Date=datetime.now(),
                        Device_Last_Online=datetime.now()
                )
                DB_Module.add(New_Module)
                DB_Module.commit()
                DB_Module.refresh(New_Module)

            else:
                Module_ID = List_Finder(Query_Module, "Module_ID")
                setattr(Query_Module, 'Last_Online_Time', datetime.now())
                setattr(Query_Module, 'Data_Count', (Query_Module.Data_Count + 1))

                # Öneri 4: Commit işlemi
                DB_Module.commit()

    except Exception as e:
        
        # Error Log
        Log.Device_Handler_Error_Log(str(e))

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
