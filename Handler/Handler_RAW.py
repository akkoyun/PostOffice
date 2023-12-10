# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Definitions
from Setup.Config import APP_Settings
from datetime import datetime
from Functions import Kafka, Log, Handler, Functions

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

    # Parse Topics
    for RAW_Message in Kafka.RAW_Consumer:

        # Handle Headers
        RAW_Headers = Definitions.Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII')
        )

        # Log Message
        Log.Terminal_Log("INFO", f"New Stream Received: {RAW_Headers.Device_ID}")

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Define Device
        Device = Definitions.Device()

        # Define DB
        with Database.DB_Session_Scope() as DB:

            # Control for Device_ID
            if Message.Info.ID is not None:

                # Set Device ID
                Device.Device_ID = Message.Info.ID

                # Set Client IP
                Device.Client_IP = RAW_Headers.Device_IP

                # Query Device
                Query_Device = DB.query(Models.Device).filter(Models.Device.Device_ID.like(Device.Device_ID)).first()

                # Control for Device
                if Query_Device is not None:

                    # Set Device Variables
                    Device.New_Device = False
                    Device.Status_ID = Query_Device.Status_ID
                    Device.Project_ID = Query_Device.Project_ID
                    Device.Model_ID = Query_Device.Model_ID
                    Device.IMEI = Query_Device.IMEI
                    Device.Last_Connection_Time = Query_Device.Last_Connection

                    # Log Message
                    Log.Terminal_Log("INFO", f"Known Device: {Device.Device_ID}")

                    # Query Version
                    Query_Version = DB.query(Models.Version).filter(Models.Version.Firmware.like(Message.Info.Firmware)).filter(Models.Version.Device_ID.like(Device.Device_ID)).first()

                    # Version Found
                    if Query_Version is not None:

                        # Set Version Variables
                        Device.New_Version = False

                        # Set Version ID
                        Device.Version_ID = Query_Device.Version_ID

                        # Log Message
                        Log.Terminal_Log("INFO", f"Known Version: {Device.Version_ID}")

                    # Version Not Found
                    else:

                        # Create New Version
                        New_Version = Models.Version(
                            Firmware = Message.Info.Firmware,
                            Device_ID = Device.Device_ID,
                        )

                        # Add Record to DataBase
                        DB.add(New_Version)

                        # Get Version ID
                        Device.Version_ID = New_Version.Version_ID

                        # Set Version Variables
                        Device.New_Version = True

                        # Log Message
                        Log.Terminal_Log("INFO", f"New Version: {Device.Version_ID}")

                    # Query Modem
                    Query_Modem = DB.query(Models.Modem).filter(Models.Modem.IMEI.like(Message.Device.IoT.IMEI)).first()

                    # Modem Found
                    if Query_Modem is not None:

                        # Log Message
                        Log.Terminal_Log("INFO", f"Known Modem: {Message.Device.IoT.IMEI}")

                        # Control Existing Version With New Version
                        if Query_Modem.Firmware != Message.Device.IoT.Firmware:

                            # Log Message
                            Log.Terminal_Log("INFO", f"New Modem Version: {Message.Device.IoT.Firmware}")

                            # Update Modem Version
                            Query_Modem.Firmware = Message.Device.IoT.Firmware

                            # Commit DataBase
                            DB.commit()
                        
                        # Modem Version is the same
                        else:

                            # Log Message
                            Log.Terminal_Log("INFO", f"Known Modem Version: {Message.Device.IoT.Firmware}")

                        # Set Modem Variables
                        Device.New_Modem = False

                    # Modem Not Found
                    else:

                        # Create New Modem
                        New_Modem = Models.Modem(
                            IMEI = Message.Device.IoT.IMEI,
                            Model_ID = 0,
                            Manufacturer_ID = 0,
                            Firmware = Message.Device.IoT.Firmware,
                        )

                        # Add Record to DataBase
                        DB.add(New_Modem)

                        # Set Modem Variables
                        Device.New_Modem = True

                        # Log Message
                        Log.Terminal_Log("INFO", f"New Modem: {Message.Device.IoT.IMEI}")

                    # Query SIM
                    Query_SIM = DB.query(Models.SIM).filter(Models.SIM.ICCID.like(Message.Device.IoT.ICCID)).first()

                    # SIM Found
                    if Query_SIM is not None:

                        # Log Message
                        Log.Terminal_Log("INFO", f"Known SIM: {Message.Device.IoT.ICCID}")

                        # Set SIM Variables
                        Device.New_SIM = False

                    # SIM Not Found
                    else:

                        # Create New SIM
                        New_SIM = Models.SIM(
                            ICCID = Message.Device.IoT.ICCID,
                            Operator_ID = 1,
                            GSM_Number = None,
                            Static_IP = None
                        )

                        # Add Record to DataBase
                        DB.add(New_SIM)

                        # Set SIM Variables
                        Device.New_SIM = True

                        # Log Message
                        Log.Terminal_Log("INFO", f"New SIM: {Message.Device.IoT.ICCID}")

                    # Update Device Last_Connection
                    Query_Device.Last_Connection = datetime.now()

                    # Commit DataBase
                    DB.commit()

                    # Log Message
                    Log.Terminal_Log("INFO", f"Device Connection Time Updated: {Query_Device.Last_Connection}")

                # Device Not Found
                else:

                    # Log Message
                    Log.Terminal_Log("INFO", f"UnKnown Device: {Device.Device_ID}")

                    # Query Version
                    Query_Version = DB.query(Models.Version).filter(Models.Version.Firmware.like(Message.Info.Firmware)).filter(Models.Version.Device_ID.like(Device.Device_ID)).first()

                    # Version Found
                    if Query_Version is not None:

                        # Log Message
                        Log.Terminal_Log("INFO", f"Version Updated: {Query_Version.Version_ID}")

                        # Set Version Variables
                        Device.New_Version = False

                        # Set Version ID
                        Device.Version_ID = Query_Device.Version_ID

                    # Version Not Found
                    else:

                        # Create New Version
                        New_Version = Models.Version(
                            Firmware = Message.Info.Firmware,
                            Device_ID = Device.Device_ID,
                        )

                        # Add Record to DataBase
                        DB.add(New_Version)

                        # Get Version ID
                        Device.Version_ID = New_Version.Version_ID

                        # Set Version Variables
                        Device.New_Version = True

                        # Log Message
                        Log.Terminal_Log("INFO", f"New Version: {Device.Version_ID}")

                    # Create New Device
                    New_Device = Models.Device(
                        Device_ID = Device.Device_ID,
                        Status_ID = 0,
                        Version_ID = Device.Version_ID,
                        Model_ID = 0,
                        IMEI = Message.Device.IoT.IMEI,
                    )

                    # Set Device Variables
                    Device.New_Device = True

                    # Log Message
                    Log.Terminal_Log("INFO", f"New Device: {Device.Device_ID} Recorded.")

            # Create New Stream
            New_Stream = Models.Stream(
                Device_ID = Device.Device_ID,
                ICCID = Device.ICCID,
                Client_IP = Device.Client_IP,
                Size = RAW_Headers.Size,
                RAW_Data = Message.dict(),
                Device_Time = RAW_Headers.Device_Time,
                Stream_Time = datetime.now()
            )

            # Add Stream to DataBase
            DB.add(New_Stream)

            # Log Message
            Log.Terminal_Log("INFO", f"New Stream: {New_Stream.Stream_ID} Recorded.")

        # Set headers
        New_Header = [
            ("Command", bytes(RAW_Headers.Command, 'utf-8')), 
            ("Device_ID", bytes(RAW_Headers.Device_ID, 'utf-8')),
            ("Device_Time", bytes(RAW_Headers.Device_Time, 'utf-8')), 
            ("Device_IP", bytes(RAW_Headers.Device_IP, 'utf-8')),
            ("Size", bytes(RAW_Headers.Size, 'utf-8')),
            ("Stream_ID", bytes(str(New_Stream.Stream_ID), 'utf-8'))
        ]

        # Send to Topic
        Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PARAMETER), Message.Device.dict(), New_Header)
        Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PAYLOAD), Message.Payload.dict(), New_Header)
        Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_DISCORD), Message.Payload.dict(), New_Header)

        # Commit Kafka Consumer
        Kafka.RAW_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"------------------------------")

# Exception
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Handle Error - {e}")

# Finally
finally:

    # Close Database
    DB_Module.close()