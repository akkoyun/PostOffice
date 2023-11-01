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

        # Log Message
        Log.Terminal_Log("INFO", f"New Stream Received...")

        # Get Headers
        RAW_Headers = Kafka.Handle_Headers(RAW_Message)

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Log Message
        Log.Terminal_Log("INFO", f"RAW Headers : {RAW_Headers}")

        # Control For Device ID
#        Device_Existance = Handler.Control_Device_Table(RAW_Headers.Device_ID)

        # Log Message
#        Log.Terminal_Log("INFO", f"Device Existance : {Device_Existance}")







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
