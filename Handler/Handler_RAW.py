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

        # Get Device Info
        Device_Info = Definitions.Device()
        Device_Info = Functions.Device_Info(RAW_Headers.Device_ID)
        Device_Info.Client_IP = RAW_Headers.Device_IP

        Log.Terminal_Log("INFO", f"Device Found: {Device_Info.Device_Found}")








        # Control for Device
        Device_Existance = Handler.Control_Device(RAW_Headers.Device_ID)

        # Control for Version
        Version_ID = Handler.Control_Version(RAW_Headers.Device_ID, Message.Info.Firmware)

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

            # Control for Version at Device
            Handler.Update_Version(RAW_Headers.Device_ID, Version_ID)

        # Device Not Found
        else:

            # Log Message
            Log.Terminal_Log("INFO", f"New Device: {Message.Info.Firmware} [{Version_ID}] / {Message.Device.IoT.IMEI} [{Modem_Status}] / {Message.Device.IoT.ICCID} [{SIM_Status}]")

            # Add Device
            Handler.Add_Device(RAW_Headers.Device_ID, Version_ID, Message.Device.IoT.IMEI)

        # Update Device Last Connection
        Handler.Update_Device_Last_Connection(RAW_Headers.Device_ID)

        # Create New Stream
        New_Stream = Models.Stream(
            Device_ID = RAW_Headers.Device_ID,
            ICCID = Message.Device.IoT.ICCID,
            Client_IP = RAW_Headers.Device_IP,
            Size = RAW_Headers.Size,
            RAW_Data = Message.dict(),
            Device_Time = RAW_Headers.Device_Time,
            Stream_Time = datetime.now()
        )

        # Add Stream to DataBase
        DB_Module.add(New_Stream)

        # Commit DataBase
        DB_Module.commit()

        # Refresh DataBase
        DB_Module.refresh(New_Stream)

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