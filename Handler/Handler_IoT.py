# Library Includes
import Setup.Functions as Functions
from Setup import Database, Models, Log, Kafka
from datetime import datetime

# IoT Handler Function
def IoT_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for IoT_Message in Kafka.Kafka_IoT_Consumer:

            # Get Headers
            IoT_Headers = Functions.Handle_Headers(IoT_Message)

            # Log Message
            Log.Terminal_Log("INFO", f"New Message Received")

            # Decode Message
            Kafka_IoT_Message = Kafka.Decode_IoT_Message(IoT_Message)

            # Define SIM ID
            SIM_ID = 0

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

                            # Log Message
                            Log.Terminal_Log("INFO", f"New SIM Added: {New_SIM.SIM_ID}")

                        # Except Error
                        except Exception as e:

                            # Log Message
                            Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

                            # Rollback DataBase
                            DB_Module.rollback()

                        # Get SIM ID
                        SIM_ID = New_SIM.SIM_ID

                    # SIM Record Found
                    else:

                        # Get SIM ID
                        SIM_ID = Query_SIM_Table.SIM_ID

                        # Log Message
                        Log.Terminal_Log("INFO", f"ICCID found. SIM ID: {SIM_ID}")

            # ICCID not found
            else:

                # Log Message
                Log.Terminal_Log("INFO", f"ICCID not found on pack.")

            # Log Message
            Log.Terminal_Log("INFO", f"SIM ID: {SIM_ID} - ICCID: {Kafka_IoT_Message.GSM.Operator.ICCID}")

            # Control for RSSI
            if Kafka_IoT_Message.GSM.Operator.RSSI is not None:
                _RSSI = Kafka_IoT_Message.GSM.Operator.RSSI
            else:
                _RSSI = 0

            # Control for Connection Time
            if Kafka_IoT_Message.GSM.Operator.ConnTime is not None:
                _ConnTime = Kafka_IoT_Message.GSM.Operator.ConnTime 
            else:
                _ConnTime = 0

            # Create New Connection Record
            New_Connection = Models.Connection(
                Device_ID = IoT_Headers.Device_ID,
                SIM_ID = SIM_ID,
                Connection_RSSI = _RSSI,
                Connection_IP = IoT_Headers.Device_IP,
                Connection_Time = _ConnTime,
                Connection_Data_Size = int(IoT_Headers.Size),
                Connection_Create_Date = IoT_Headers.Device_Time
            )

            # Add Record to DataBase
            try:

                # Add Record to DataBase
                DB_Module.add(New_Connection)

                # Database Flush
                DB_Module.flush()

                # Commit DataBase
                DB_Module.commit()

                # Commit Queue
                Kafka.Kafka_IoT_Consumer.commit()

                # Log Message
                Log.Terminal_Log("INFO", f"New Connection Added: {New_Connection.Connection_ID}")

            except Exception as e:

                # Log Message
                Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

                # Rollback DataBase
                DB_Module.rollback()

            finally:

                # Close Database
                DB_Module.close()

            # Log Message
            Log.Terminal_Log("INFO", f"---------------------------------------")

    finally:

        # Close Database
        DB_Module.close()

# Handle Device
IoT_Handler()
