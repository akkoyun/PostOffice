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

        # Log Message
        Log.Terminal_Log("INFO", f"---------- Parameters ----------")
        Log.Terminal_Log("INFO", f"Device Time: {RAW_Headers.Device_Time}")

        # Decode Message
        Message = Kafka.Decode_Device_Message(RAW_Message)

        # Control for B_IV
        if Message.Power.B_IV is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_IV", Message.Power.B_IV)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_IV - {Message.Power.B_IV}")

        # Control for B_AC
        if Message.Power.B_AC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_AC", Message.Power.B_AC)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_AC - {Message.Power.B_AC}")

        # Control for B_FC
        if Message.Power.B_FC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_FC", Message.Power.B_FC)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_FC - {Message.Power.B_FC}")

        # Control for B_IC
        if Message.Power.B_IC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_IC", Message.Power.B_IC)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_IC - {Message.Power.B_IC}")

        # Control for B_SOC
        if Message.Power.B_SOC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_SOC", Message.Power.B_SOC)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_SOC - {Message.Power.B_SOC}")

        # Control for B_T
        if Message.Power.B_T is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_T", Message.Power.B_T)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_T - {Message.Power.B_T}")

        # Control for B_CS
        if Message.Power.B_CS is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "B_CS", Message.Power.B_CS)
            Log.Terminal_Log("INFO", f"New Parameter Received: B_CS - {Message.Power.B_CS}")

        # Control for RSSI
        if Message.IoT.RSSI is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "RSSI", Message.IoT.RSSI)
            Log.Terminal_Log("INFO", f"New Parameter Received: RSSI - {Message.IoT.RSSI}")
        
        # Control for ConnTime
        if Message.IoT.ConnTime is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "ConnTime", Message.IoT.ConnTime)
            Log.Terminal_Log("INFO", f"New Parameter Received: ConnTime - {Message.IoT.ConnTime}")

        # Control for TAC
        if Message.IoT.TAC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "TAC", Message.IoT.TAC)
            Log.Terminal_Log("INFO", f"New Parameter Received: TAC - {Message.IoT.TAC}")
        
        # Control for LAC
        if Message.IoT.LAC is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "LAC", Message.IoT.LAC)
            Log.Terminal_Log("INFO", f"New Parameter Received: LAC - {Message.IoT.LAC}")

        # Control for CellID
        if Message.IoT.Cell_ID is not None: 
            Handler.Parameter_Recorder(RAW_Headers.Stream_ID, RAW_Headers.Device_Time, "Cell_ID", Message.IoT.Cell_ID)
            Log.Terminal_Log("INFO", f"New Parameter Received: Cell_ID - {Message.IoT.Cell_ID}")

        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

finally:

    # Close Database
    DB_Module.close()
