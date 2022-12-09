# Import Libraries
from Config import Kafka_Power_Consumer
from Database import SessionLocal, DB_Engine
import Models, Schema, json

# Create DB Models
Models.Base.metadata.create_all(bind=DB_Engine)

# Battery Parser Function
def Power_Parser():

    try:

        for Message in Kafka_Power_Consumer:

            # handle Message.
            Kafka_Power_Message = Schema.IoT_Data_Pack_Power(**json.loads(Message.value.decode()))

            # Handle Headers
            Command = Message.headers[0][1].decode('ASCII')
            Device_ID = Message.headers[1][1].decode('ASCII')
            Device_Time = Message.headers[2][1].decode('ASCII')
            Device_IP = Message.headers[3][1].decode('ASCII')

            # Print LOG
            print("-----------------------------------------------------------------------------------------------------")
            print("Device_ID : ", Device_ID, " Device Time : ", Device_Time)
            print("Command : ", Command, " IP : ", Device_IP)
            print("Topic : ", Message.topic, " - Partition : ", Message.partition, " - Offset : ", Message.offset)
            print("-----------------------------------------------------------------------------------------------------")
            print(Kafka_Power_Message)

            # Create Add Record Command
            New_Battery_Post = Models.Device_Battery(
                Device_Time = Device_Time, 
                Device_ID = Device_ID, 
                IV = Kafka_Power_Message.Battery.IV,
                AC = Kafka_Power_Message.Battery.AC,
                SOC = Kafka_Power_Message.Battery.SOC,
                Charge = Kafka_Power_Message.Battery.Charge,
                T = Kafka_Power_Message.Battery.T,
                FB = Kafka_Power_Message.Battery.FB,
                IB = Kafka_Power_Message.Battery.IB)

            # Add and Refresh DataBase
            db = SessionLocal()
            db.add(New_Battery_Post)
            db.commit()
            db.refresh(New_Battery_Post)

            # Print LOG
            print("Message recorded to Battery DB with Battery_ID : ", New_Battery_Post.Info_ID)
            print("-----------------------------------------------------------------------------------------------------")

            # Close Database
            db.close()

            # Commit Message
            Kafka_Power_Message.commit()

    finally:
        print("Error Accured !!")


# Handle All Message in Topic
Power_Parser()

