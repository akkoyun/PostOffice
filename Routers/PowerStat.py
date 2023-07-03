# Library Includes
from Setup import Database, Models, Log, Schema
from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocket
import json

# Define FastAPI Object
PostOffice_PowerStat = APIRouter()

# WebSockets Connections
Connections = {}

# IoT WebSockets Method
@PostOffice_PowerStat.websocket("/PowerStat/{Device_ID}")
async def PowerStat_WS(websocket: WebSocket, Device_ID: str):

	# Accept Connection
	await websocket.accept()

    # Connection set and add to list
	Connections[Device_ID] = websocket

	# Log Message
	Log.WebSocket_Data_Log(Device_ID, "Connected", "In")

    # Try to Receive Message
	try:

        # Receive Message
		while True:

			# Receive Message
			Message = await websocket.receive_json()

			# Handle Company
			try:
				Company = Message["Command"].split(":")[0]
			except:
				Company = "Unknown"

			# Handle Device
			try:
				Device = Message["Command"].split(":")[1].split(".")[0]
			except:
				Device = "Unknown"

            # Handle Command
			try:
				Command = Message["Command"].split(":")[1].split(".")[1]
			except:
				Command = "Unknown"

			# Device is PowerStat
			if Device == "PowerStat":

				# Create Add Record Command
				New_Buffer = Models.Valid_Data_Buffer(
					Buffer_Device_ID = Device_ID,
					Buffer_Client_IP = websocket.client.host,
					Buffer_Company = Company,
					Buffer_Device = Device,
					Buffer_Command = Command,
					Buffer_Data = str(Message),)

				# Define DB
				DB_Buffer = Database.SessionLocal()

				# Add and Refresh DataBase
				DB_Buffer.add(New_Buffer)
				DB_Buffer.commit()
				DB_Buffer.refresh(New_Buffer)

				# Close Database
				DB_Buffer.close()

				# Handle Sunscribe Command
				if Command == "Subscribe":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Subscribe", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})

				# Handle Battery Command
				elif Command == "Battery":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Battery", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})
				
				# Handle Energy Command
				elif Command == "Energy":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Energy", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})

				# Handle Operator Command
				elif Command == "Operator":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Operator", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})

				# Handle Pressure Command
				elif Command == "Pressure":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Pressure", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})

				# Handle Status Command
				elif Command == "Status":

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Status", "In")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_200_OK})

				# Handle Undefined Command
				else:

					# Log Message
					Log.WebSocket_Data_Log(Device_ID, "Undefined Command")

					# Send Sample Response
					await websocket.send_json({"Event": status.HTTP_405_METHOD_NOT_ALLOWED})

			# Device is not PowerStat
			else:

				# Log Message
				Log.WebSocket_Data_Log(Device_ID, "Wrong Device", "In")

				# Create Add Record Command
				New_Buffer = Models.Wrong_Data_Buffer(
					Buffer_Client_IP = websocket.client.host,
					Buffer_Data = str(Message))

				# Define DB
				DB_Buffer = Database.SessionLocal()

				# Add and Refresh DataBase
				DB_Buffer.add(New_Buffer)
				DB_Buffer.commit()
				DB_Buffer.refresh(New_Buffer)

				# Close Database
				DB_Buffer.close()

				# Send Sample Response
				await websocket.send_json({"Event": status.HTTP_406_NOT_ACCEPTABLE})

    # If Disconnect
	except WebSocketDisconnect:

		# Log Message
		Log.WebSocket_Data_Log(Device_ID, "Disconnected", "In")

	# If Error
	finally:

		# Delete Connection
		del Connections[Device_ID]

# IoT Start Command
@PostOffice_PowerStat.post("/PowerStat/Command/{Device_ID}")
async def Send_Start_Command(Data: Schema.WebSocket_Command_Model, Device_ID: str):

	# Decide Broadcast or Command
	if Device_ID == "Broadcast":
		
		# Log Message
		Log.WebSocket_Data_Log("BroadCast", Data.Command, "Out")

		# Send Sample Response
		for Connection in Connections.values():

			# Send Sample Response
			await Connection.send_text(Data.json())

		# Send Success
		return {"Status": 200, "Device_Count": len(Connections)}

	# Command
	else:

		# Log Message
		Log.WebSocket_Data_Log(Device_ID, Data.Command, "Out")

		# Select Device
		if Device_ID in Connections:

			# Select Connection
			Device_Connection = Connections[Device_ID]

			# Send Sample Response
			await Device_Connection.send_text(Data.json())

			# Send Success
			return {"Status": 200}

		# Not Found
		else:

			# Send Success
			return {"Status": 400}

# IoT Post Service Health Check
@PostOffice_PowerStat.get("/PowerStat/")
async def get():

	# Log Message
	Log.WebSocket_Data_Log(0, "Status", "In")

	# Send Success
	return {"Service": "PostOffice", 
	 		"Version": "02.00.00", 
			"Status": "Online", 
			"Active": len(Connections),
			"Connections": list(Connections.keys())}
