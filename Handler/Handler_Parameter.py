# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database
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

        # Get Device Time
        Device_Time = RAW_Headers.Device_Time

        # Log Message
        Log.Terminal_Log("INFO", f"---------- Parameters ----------")

        # Decode Message
        Message = Kafka.Decode_Device_Message(RAW_Message)

        # Control for Payload
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_IV", Message.Power.B_IV)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_AC", Message.Power.B_AC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_FC", Message.Power.B_FC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_IC", Message.Power.B_IC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_SOC", Message.Power.B_SOC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_T", Message.Power.B_T)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "B_CS", Message.Power.B_CS)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "RSSI", Message.IoT.RSSI)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "ConnTime", Message.IoT.ConnTime)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "TAC", Message.IoT.TAC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "LAC", Message.IoT.LAC)
        Handler.Parameter_Recorder(RAW_Headers.Stream_ID, Device_Time, "Cell_ID", Message.IoT.Cell_ID)

        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

finally:

    # Close Database
    DB_Module.close()
