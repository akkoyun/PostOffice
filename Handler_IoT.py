# Library Includes
import Setup.Functions as Functions
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
from datetime import datetime

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('Device.IoT', bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}", group_id="IoT_Consumer", auto_offset_reset='latest', enable_auto_commit=False)

# IoT Handler Function
def IoT_Handler():

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka_Consumer:

            # Define SIM ID
            SIM_ID = 0

            # Define DB
            DB_Module = Database.SessionLocal()

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
    
                        # Except Error
                        except Exception as e:

                            # Log Message
                            print(f"An error occurred while adding SIM: {e}")

                            # Rollback DataBase
                            DB_Module.rollback()

                        # Get SIM ID
                        SIM_ID = New_SIM.SIM_ID

                    # SIM Record Found
                    else:

                        # Get SIM ID
                        SIM_ID = Query_SIM_Table.SIM_ID

            # Control for RSSI
            if Kafka_IoT_Message.GSM.Operator.RSSI is not None:
                _RSSI = Kafka_IoT_Message.GSM.Operator.RSSI
            else:
                _RSSI = 0

            # Control for IP
            if Kafka_IoT_Message.GSM.Operator.IP is not None:
                _IP = Kafka_IoT_Message.GSM.Operator.IP
            else:
                _IP = ""

            # Control for Connection Time
            if Kafka_IoT_Message.GSM.Operator.ConnTime is not None:
                _ConnTime = Kafka_IoT_Message.GSM.Operator.ConnTime 
            else:
                _ConnTime = 0

            # Create New Connection Record
            New_Connection = Models.Connection(
                Device_ID = Headers.Device_ID,
                SIM_ID = SIM_ID,
                Connection_RSSI = _RSSI,
                Connection_IP = _IP,
                Connection_Time = _ConnTime,
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

            # Close Database
            DB_Module.close()

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
IoT_Handler()
