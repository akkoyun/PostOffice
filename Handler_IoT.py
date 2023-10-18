# Library Includes
from Setup import Database, Models, Log, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer
import json

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
            Kafka_IoT_Message = Schema.Pack_IoT(**Parsed_Json)

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
                    New_Data_Stream_ID = Message.headers[5][1].decode('ASCII')

            # If not, log the error and skip to the next iteration
            else:
                
                # Log Message
                print(f"Header Error")
                
                # Skip to the next iteration
                continue

            # Control for SIM Record
            # ----------------------

            # Control for ICCID
            if Kafka_IoT_Message.GSM.Operator.ICCID is not None:
    
                    # Define Colomns
                    # SIM_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
                    # SIM_ICCID = Column(String, nullable=False)
                    # MCC_ID = Column(Integer, nullable=False)
                    # MNC_ID = Column(Integer, nullable=False)
                    # SIM_Number = Column(String, nullable=True)
                    # SIM_Static_IP = Column(String, nullable=True)
                    # SIM_Status = Column(Boolean, nullable=False, server_default=text('false'))
                    # SIM_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

                    # Query SIM Table
                    Query_SIM_Table = DB_Module.query(Models.SIM).filter(Models.SIM.SIM_ICCID.like(Kafka_IoT_Message.GSM.Operator.ICCID)).first()
    
                    # SIM Record Not Found
                    if not Query_SIM_Table:
    
                        # Create New SIM Record
                        New_SIM = Models.SIM(
                            SIM_ICCID = Kafka_IoT_Message.GSM.Operator.ICCID,
                            SIM_MCC = Kafka_IoT_Message.GSM.Operator.MCC,
                            SIM_MNC = Kafka_IoT_Message.GSM.Operator.MNC,
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

            # Add Record to Connection Table
            # ------------------------------

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
