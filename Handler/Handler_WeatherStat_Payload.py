# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Functions as Functions
from Setup import Database, Log, Kafka
from datetime import datetime

# Power Measurement Handler Function
def Power_Handler():

    # Handle Messages
    try:

        # Define DB
        DB_Module = Database.SessionLocal()

        # Parse Messages
        for Message in Kafka.Kafka_WeatherStat_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Log Message
            Log.Terminal_Log("INFO", f"New Message Received")

            # Decode Message
            Kafka_WeatherStat_Payload_Message = Kafka.Decode_WeatherStat_Payload_Message(Message)

            # Add AT Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.AT is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'AT', Kafka_WeatherStat_Payload_Message.Environment.AT)

            # Add AH Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.AH is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'AH', Kafka_WeatherStat_Payload_Message.Environment.AH)

            # Add AP Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.AP is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'AP', Kafka_WeatherStat_Payload_Message.Environment.AP)

            # Add UV Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.UV is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'UV', Kafka_WeatherStat_Payload_Message.Environment.UV)

            # Add VL Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.VL is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'VL', Kafka_WeatherStat_Payload_Message.Environment.VL)

            # Add IL Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.IL is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'IL', Kafka_WeatherStat_Payload_Message.Environment.IL)

            # Add R Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.R is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'R', Kafka_WeatherStat_Payload_Message.Environment.R)

            # Add WS Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.WS is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'WS', Kafka_WeatherStat_Payload_Message.Environment.WS)

            # Add WD Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.WD is not None:

                # Add Measurement Record
                Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, 'WD', Kafka_WeatherStat_Payload_Message.Environment.WD)

            # Add ST Measurement Record
            if Kafka_WeatherStat_Payload_Message.Environment.ST is not None:

                # Loop Through Measurements
                for index, ST_Value in enumerate(Kafka_WeatherStat_Payload_Message.Environment.ST):

                    # Set Dynamic Variable Name
                    ST_Variable_Name = f"ST{index}"

                    # Add Measurement Record
                    Functions.Add_WeatherStat_Measurement(Headers.Data_Stream_ID, Headers.Device_ID, Headers.Device_Time, ST_Variable_Name, ST_Value)

            # Log Message
            Log.Terminal_Log("INFO", f"-----------------------------------------------------------")

            # Log to Queue
            Kafka.Send_To_Log_Topic(Headers.Device_ID, f"WeatherStat Measurements Saved : {Headers.Device_IP}")

            # Commit Queue
            Kafka.Kafka_WeatherStat_Consumer.commit()

    finally:

        # Log Message
        Log.LOG_Error_Message(f"Handle Error - {datetime.now()}")

        # Close Database
        DB_Module.close()

# Handle Device
Power_Handler()
