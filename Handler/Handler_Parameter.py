# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Definitions
from Functions import Kafka, Log, Handler, Functions
from Setup.Definitions import Type_List

# Try to Parse Topics
try:

    # Parse Topics
    for RAW_Message in Kafka.Parameter_Consumer:

        # Handle Headers
        RAW_Headers = Definitions.Handler_Headers(
            RAW_Message.headers[0][1].decode('ASCII'),
            RAW_Message.headers[1][1].decode('ASCII'),
            RAW_Message.headers[2][1].decode('ASCII'),
            RAW_Message.headers[3][1].decode('ASCII'),
            RAW_Message.headers[4][1].decode('ASCII'),
            RAW_Message.headers[5][1].decode('ASCII'),
            RAW_Message.headers[6][1].decode('ASCII'),
            RAW_Message.headers[7][1].decode('ASCII'),
        )

        # Convert Device Time (str) to datetime
        Device_Time = RAW_Headers.Device_Time.replace("T", " ").replace("Z", "")

        # Decode Message
        Message = Kafka.Decode_Device_Message(RAW_Message)

        # 2 - Control for Power Variables
        for Type_ID, Variable, Description, Unit, Segment_ID in Definitions.Variable_List(2):

            # Try to Record
            try:

                # Set Data Pack
                Measurement = Definitions.Measurement_Class(
                    type_id=Type_ID, 
                    variable=Variable, 
                    path=f"Message.Power.{Variable}",
                    value=eval(f"Message.Power.{Variable}"),
                    description=Description, 
                    unit=Unit, 
                    segment_id=Segment_ID,
                    stream_id=RAW_Headers.Stream_ID,
                    device_time=Device_Time
                )

                # Record Payload
                Functions.Parameter_Recorder(Measurement)

            # Handle Errors
            except:
                pass

        # 3 - Control for IoT Variables
        for Type_ID, Variable, Description, Unit, Segment_ID in Definitions.Variable_List(3):

            # Try to Record
            try:

                # Set Data Pack
                Measurement = Definitions.Measurement_Class(
                    type_id=Type_ID, 
                    variable=Variable, 
                    path=f"Message.IoT.{Variable}",
                    value=eval(f"Message.IoT.{Variable}"),
                    description=Description, 
                    unit=Unit, 
                    segment_id=Segment_ID,
                    stream_id=RAW_Headers.Stream_ID,
                    device_time=Device_Time
                )

                # Record Payload
                Functions.Parameter_Recorder(Measurement)

            # Handle Errors
            except:
                pass

        # Commit Kafka Consumer
        Kafka.Parameter_Consumer.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"******************************")

# Handle Errors
except Exception as e:

    # Log Message
    Log.Terminal_Log("ERROR", f"Parameter Handler Error: {e}")
