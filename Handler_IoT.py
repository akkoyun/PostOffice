# Library Includes
import Setup.Functions as Functions
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('Device.IoT',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="IoT_Consumer",
                               auto_offset_reset='latest',
                               enable_auto_commit=False)

# IoT Handler Function
def IoT_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Decode Message
            Kafka_IoT_Message = Functions.Decode_IoT_Message(Message, Kafka_Consumer, Schema)

            # Control for ICCID
            if Kafka_IoT_Message.GSM.Operator.ICCID is not None:

                    # Query SIM Table
                    Query_SIM_Table = DB_Module.query(Models.SIM).filter(Models.SIM.SIM_ICCID.like(Kafka_IoT_Message.GSM.Operator.ICCID)).first()
    
                    # SIM Record Not Found
                    if not Query_SIM_Table:
    
                        # Create New SIM Record
                        New_SIM = Models.SIM(
                            SIM_ICCID = Kafka_IoT_Message.GSM.Operator.ICCID,
                            MCC_ID = Kafka_IoT_Message.GSM.Operator.MCC,
                            MNC_ID = Kafka_IoT_Message.GSM.Operator.MNC,
                            SIM_Create_Date = Headers.Device_Time
                        )
    
                        # Add Record to DataBase
                        DB_Module.add(New_SIM)
    
                        # Commit DataBase
                        DB_Module.commit()
    
                        # Refresh DataBase
                        DB_Module.refresh(New_SIM)

                    # SIM Record Found
                    else:

                        # Get SIM ID
                        SIM_ID = getattr(Query_SIM_Table, "SIM_ID", None)

            print(SIM_ID)

            # Create New Connection Record
            New_Connection = Models.Connection(
                Device_ID = Headers.Device_ID,
                SIM_ID = SIM_ID,
                Connection_RSSI = Kafka_IoT_Message.GSM.Operator.RSSI,
                Connection_IP = Kafka_IoT_Message.GSM.Operator.IP,
                Connection_Time = Kafka_IoT_Message.GSM.Operator.Time,
                Connection_Data_Size = int(Headers.Size),
                Connection_Create_Date = Headers.Device_Time
            )
        
            # Add Record to DataBase
            DB_Module.add(New_Connection)

            # Commit DataBase
            DB_Module.commit()

            # Refresh DataBase
            DB_Module.refresh(New_Connection)

            # Commit Queue
            Kafka_Consumer.commit()



    finally:

        # Close Database
        DB_Module.close()            

# Handle Device
IoT_Handler()
