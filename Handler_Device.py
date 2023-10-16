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

class Headers:
    def __init__(self, headers):
        self.Command = headers[0][1].decode('ASCII')
        self.Device_ID = headers[1][1].decode('ASCII')
        self.Device_Time = headers[2][1].decode('ASCII')
        self.Device_IP = headers[3][1].decode('ASCII')
        self.Size = headers[4][1].decode('ASCII')


# Parser Function
def Device_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    try:
        for Message in Kafka_Consumer:

            Raw_Message_JSON = json.loads(Message.value.decode())

            # Handle Message
            Kafka_Message = Schema.Data_Pack_Model(**Raw_Message_JSON)

            # Handle Headers
            msg_headers = Headers(Message.headers)

            # Database Query
            Query_Module = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(msg_headers.Device_ID)).first()

            if not Query_Module:
                New_Module = Models.Module(
                        Device_ID=msg_headers.Device_ID,
                        Device_Data_Count=1,
                        Device_Create_Date=datetime.now(),
                        Device_Last_Online=datetime.now()
                )
                DB_Module.add(New_Module)
                DB_Module.commit()
                DB_Module.refresh(New_Module)

                Module_ID = getattr(New_Module, "Module_ID", None)

            else:
                Module_ID = getattr(Query_Module, "Module_ID", None)
                setattr(Query_Module, 'Last_Online_Time', datetime.now())
                setattr(Query_Module, 'Data_Count', (Query_Module.Data_Count + 1))

                DB_Module.commit()

            # Log Message
            Log.Device_Handler_Log(str(Module_ID))

    except Exception as e:

        # Error Log
        Log.Device_Handler_Error_Log(str(e))

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
Device_Handler()
