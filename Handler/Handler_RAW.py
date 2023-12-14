# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Definitions, Schema
from Setup.Config import APP_Settings
from datetime import datetime
from Functions import Kafka, Log, Functions

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
            RAW_Message.headers[5][1].decode('ASCII'),
        )

        # Define Device
        Device = Definitions.Device()

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Set Device Variables
        Device.Device_ID = Header.Device_ID
        Device.Client_IP = Header.Device_IP
        Device.Firmware = Message.Info.Firmware
        Device.IMEI = Message.Device.IoT.IMEI
        Device.ICCID = Message.Device.IoT.ICCID
        Device.Modem_Firmware = Message.Device.IoT.Firmware

        # Control Device
        Functions.Control_Device(Device)

        # Control Version
        Functions.Update_Version(Device)

        # Control for Modem
        Functions.Update_Modem(Device)

        # Control for SIM
        Functions.Update_SIM(Device)

        # Log Message
        Log.Terminal_Log("INFO", f"Device ID      : {Device.Device_ID} [{Device.New_Device}]")
        Log.Terminal_Log("INFO", f"Device Time    : {Device.Last_Connection_Time}")
        Log.Terminal_Log("INFO", f"Device IP      : {Header.Device_IP}")
        Log.Terminal_Log("INFO", f"Size           : {Header.Size} byte")
        Log.Terminal_Log("INFO", f"Firmware       : {Device.Firmware} [{Device.New_Version}]")
        Log.Terminal_Log("INFO", f"IMEI           : {Device.IMEI} [{Device.New_Modem}] / {Device.Modem_Firmware}")
        Log.Terminal_Log("INFO", f"SIM            : {Device.ICCID} [{Device.New_SIM}]")
        Log.Terminal_Log("INFO", f"Status         : {Device.Status_ID}")
        Log.Terminal_Log("INFO", f"Project ID     : {Device.Project_ID}")
        Log.Terminal_Log("INFO", f"------------------------------------------------------------")

        # Add Stream to DataBase
        Stream_ID = Functions.Record_Stream(Header.Device_ID, Message.Device.IoT.ICCID, Header.Device_IP, Header.Size, Header.Body, Message.Info.TimeStamp)

        # Set headers
        New_Header = [
            ("Command", bytes(Header.Command, 'utf-8')), 
            ("Device_ID", bytes(Header.Device_ID, 'utf-8')),
            ("Device_Time", bytes(Header.Device_Time, 'utf-8')), 
            ("Device_IP", bytes(Header.Device_IP, 'utf-8')),
            ("Size", bytes(Header.Size, 'utf-8')),
            ("Stream_ID", bytes(str(Stream_ID), 'utf-8')),
            ("Status_ID", bytes(str(Device.Status_ID), 'utf-8')),
            ("Project_ID", bytes(str(Device.Project_ID), 'utf-8'))
       ]

        # Send to Topic
        Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PARAMETER), Message.Device.dict(), New_Header)
        Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PAYLOAD), Message.Payload.dict(), New_Header)
        if Device.Status_ID != 1: Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_DISCORD), Message.Payload.dict(), New_Header)

        # Commit Kafka Consumer
        Kafka.RAW_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"************************************************************")

# Exception
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Handle Error - {e}")

# Finally
finally:

    # Close Database
    DB_Module.close()