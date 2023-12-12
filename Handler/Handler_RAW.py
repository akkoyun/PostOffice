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
        Header = Definitions.Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII')
        )

        # Log Message
        Log.Terminal_Log("INFO", f"New Stream Received: {Header.Device_ID}")

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Control Version
        Version_ID = Functions.Update_Version(Header.Device_ID, Message.Info.Firmware)



























        # Control for Device
        Device_Existance = Handler.Control_Device(Header.Device_ID)

        # Control for Modem
        Modem_Existance = Handler.Control_Modem(Message.Device.IoT.IMEI, Message.Device.IoT.Firmware)

        # Control for SIM
        SIM_Existance = Handler.Control_SIM(Message.Device.IoT.ICCID)

        # Declare Log Messages
        Modem_Status = "New" if Modem_Existance else "Old"
        SIM_Status = "New" if SIM_Existance else "Old"

        # Device Found
        if Device_Existance:

            # Log Message
            Log.Terminal_Log("INFO", f"Device Found: {Message.Info.Firmware} [{Version_ID}] / {Message.Device.IoT.IMEI} [{Modem_Status}] / {Message.Device.IoT.ICCID} [{SIM_Status}]")

        # Device Not Found
        else:

            # Log Message
            Log.Terminal_Log("INFO", f"New Device: {Message.Info.Firmware} [{Version_ID}] / {Message.Device.IoT.IMEI} [{Modem_Status}] / {Message.Device.IoT.ICCID} [{SIM_Status}]")

            # Add Device
            Handler.Add_Device(Header.Device_ID, Version_ID, Message.Device.IoT.IMEI)

        # Update Device Last Connection
        Handler.Update_Device_Last_Connection(Header.Device_ID)





        # Set headers
        New_Header = [
            ("Command", bytes(Header.Command, 'utf-8')), 
            ("Device_ID", bytes(Header.Device_ID, 'utf-8')),
            ("Device_Time", bytes(Header.Device_Time, 'utf-8')), 
            ("Device_IP", bytes(Header.Device_IP, 'utf-8')),
            ("Size", bytes(Header.Size, 'utf-8')),
            ("Stream_ID", bytes(str(Header.Stream_ID), 'utf-8'))
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