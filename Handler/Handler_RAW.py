# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Definitions
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

        # Log Message
        Log.Terminal_Log("INFO", f"Device ID   : {Header.Device_ID}")
        Log.Terminal_Log("INFO", f"Command     : {Header.Command}")
        Log.Terminal_Log("INFO", f"Device Time : {Header.Device_Time}")
        Log.Terminal_Log("INFO", f"Device IP   : {Header.Device_IP}")
        Log.Terminal_Log("INFO", f"Size        : {Header.Size}")
        Log.Terminal_Log("INFO", f"------------------------------")

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Control Device
        Functions.Control_Device(Header.Device_ID)

        # Control Version
        Functions.Update_Version(Header.Device_ID, Message.Info.Firmware)




















        # Control for Modem
#        Functions.Update_Modem(Header.Device_ID, Message.Device.IoT.IMEI, Message.Device.IoT.Firmware)

        # Control for SIM
#        Functions.Update_SIM(Message.Device.IoT.ICCID)

        # Add Stream to DataBase
#        Stream_ID = Functions.Record_Stream(Header.Device_ID, Message.Device.IoT.ICCID, Header.Device_IP, Header.Size, Clean_RAW_Body, Message.Device.Device_Time)

        # Set headers
#        New_Header = [
#           ("Command", bytes(Header.Command, 'utf-8')), 
#           ("Device_ID", bytes(Header.Device_ID, 'utf-8')),
#           ("Device_Time", bytes(Header.Device_Time, 'utf-8')), 
#           ("Device_IP", bytes(Header.Device_IP, 'utf-8')),
#           ("Size", bytes(Header.Size, 'utf-8')),
#           ("Stream_ID", bytes(str(Stream_ID), 'utf-8'))
#       ]

        # Send to Topic
#       Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PARAMETER), Message.Device.dict(), New_Header)
#       Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_PAYLOAD), Message.Payload.dict(), New_Header)
#       Kafka.Send_To_Topic(str(APP_Settings.KAFKA_TOPIC_DISCORD), Message.Payload.dict(), New_Header)

        # Commit Kafka Consumer
#       Kafka.RAW_Consumer.commit()

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