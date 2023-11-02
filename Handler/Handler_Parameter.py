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
    for RAW_Message in Kafka.Parameter_Consumer:

        # Handle Headers
        RAW_Headers = Kafka.Handler_Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII')
        )

        # Log Message
        Log.Terminal_Log("INFO", f"New Parameter Received: {RAW_Headers.Device_ID}")

        # Decode Message
        Message = Kafka.Decode_RAW_Message(RAW_Message)

        # Control for B_IV
        if Message.Device.Power.B_IV is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_IV", Message.Device.Power.B_IV)

        # Control for B_AC
        if Message.Device.Power.B_AC is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_AC", Message.Device.Power.B_AC)

        # Control for B_FC
        if Message.Device.Power.B_FC is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_FC", Message.Device.Power.B_FC)

        # Control for B_IC
        if Message.Device.Power.B_IC is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_IC", Message.Device.Power.B_IC)

        # Control for B_SOC
        if Message.Device.Power.B_SOC is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_SOC", Message.Device.Power.B_SOC)

        # Control for B_T
        if Message.Device.Power.B_T is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_T", Message.Device.Power.B_T)

        # Control for B_CS
        if Message.Device.Power.B_CS is not None: Handler.Parameter_Recorder(RAW_Headers.Stream_ID, "B_CS", Message.Device.Power.B_CS)










        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"***********************************************************************************")

finally:

    # Log Message
    Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

    # Close Database
    DB_Module.close()
