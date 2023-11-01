# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models
from datetime import datetime
from Functions import Kafka, Log, Handler

# Try to Parse Topics
try:

    # Define DB
    DB_Module = Database.SessionLocal()

    # Parse Topics
    for RAW_Message in Kafka.RAW_Consumer:

        # Handle Headers
        RAW_Headers = Kafka.Headers(
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

        # Control for Device
        Device_Existance = Handler.Control_Device(RAW_Headers.Device_ID)

        # Control for Version
        Version_ID = Handler.Control_Version(RAW_Headers.Device_ID, Message.Info.Firmware)

        # Control for Modem
        Modem_Existance = Handler.Control_Modem(Message.Device.IoT.IMEI)

        # Control for SIM
        SIM_Existance = Handler.Control_SIM(Message.Device.IoT.ICCID)

        # Device Found
        if Device_Existance:

            # Log Message
            Log.Terminal_Log("INFO", f"Device Found: {Message.Info.Firmware} [{Version_ID}] / {Message.Device.IoT.IMEI} [{Modem_Existance}] / {Message.Device.IoT.ICCID} [{SIM_Existance}]")

            # Control for Version at Device
            Handler.Update_Version(RAW_Headers.Device_ID, Version_ID)

        # Device Not Found
        else:

            # Log Message
            Log.Terminal_Log("INFO", f"New Device: {Message.Info.Firmware} [{Version_ID}] / {Message.Device.IoT.IMEI} [{Modem_Existance}] / {Message.Device.IoT.ICCID} [{SIM_Existance}]")

            # Add Device
            Handler.Add_Device(RAW_Headers.Device_ID, Version_ID, Message.Device.IoT.IMEI)






















        # Log Message
        Log.Terminal_Log("INFO", f"****************************************")



        # Cihazı device tablosundan kontrol et
            # yok ise cihazı varsayılan değerler ile ekle
            # var ise versyonu düzenle
        # ICCID tablosundan simi kontrol et
            # yok ise simi varsayılan değerler ile ekle






        # Commit Kafka Consumer
        Kafka.RAW_Consumer.commit()


finally:

    # Log Message
    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

    # Close Database
    DB_Module.close()
