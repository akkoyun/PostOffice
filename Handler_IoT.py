# Library Includes
import Setup.Functions as Functions
from Setup import Database, Models, Schema
from Setup.Config import APP_Settings
from kafka import KafkaConsumer

# Create DB Models
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Kafka Consumer
Kafka_Consumer = KafkaConsumer('Device.IoT',
                               bootstrap_servers=f"{APP_Settings.POSTOFFICE_KAFKA_HOSTNAME}:{APP_Settings.POSTOFFICE_KAFKA_PORT}",
                               group_id="IoT_Consumer",
                               auto_offset_reset='latest',
                               enable_auto_commit=False)

# IoT Handler Function
def IoT_Handler():

    # Define DB
    DB_Module = Database.SessionLocal()

    # Handle Messages
    try:

        # Parse Messages
        for Message in Kafka_Consumer:

            # Get Headers
            Headers = Functions.Handle_Full_Headers(Message)

            # Decode Message
            Kafka_IoT_Message = Functions.Decode_Message(Message, Kafka_Consumer, Schema)

            print(Kafka_IoT_Message)




    finally:

        # Close Database
        DB_Module.close()            

# Handle Device
IoT_Handler()
