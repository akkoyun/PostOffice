def Log_API_Online():

    # LOG
	print("------------------------------------------------")
	print("Kafka IoT Data Producer - ONLINE")
	print("------------------------------------------------")

def Log_API_Offline():

	# LOG
	print("------------------------------------------------")
	print("Kafka IoT Data Producer - OFFLINE")
	print("------------------------------------------------")

def Log_API_Error():

    # Print LOG
    print("API Error --> Sended to Kafka Error Queue..")

def Log_API_Incomming_Data(TimeStamp, ID, Command):

	print("Incomming Data -->", TimeStamp, " : ", ID, " - ", Command, " --> Sended to Queue..")
