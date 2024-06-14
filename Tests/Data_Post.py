from fastapi.testclient import TestClient
from PostOffice.PostOffice import PostOffice

# Define Test Client
Test_Client = TestClient(PostOffice)

# Define Test Cases
def Data_Post():

	# Define Data
	Data = {
		"Info": {
			"Command": "Timed",
			"TimeStamp": "2024-03-20 14:40:49",
			"ID": "C50000011D05A970",
			"Firmware": "04.00.20"
		},
		"Device": {
			"Power": {
				"B_IV": 4.16,
				"B_AC": 0.47,
				"B_IC": 1600,
				"B_FC": 1500,
				"B_SOC": 99.00,
				"B_T": 24.50,
				"B_CS": 3
			},
			"IoT": {
				"Firmware": "25.30.226",
				"IMEI": "354485417649444",
				"ICCID": "8990011936290169339",
				"RSSI": 66,
				"WDS": 3,
				"ConnTime": 3.724,
				"MCC": 286,
				"MNC": 1,
				"TAC": 8770,
				"CELLID": 53541
			}
		},
		"Payload": {
			"PCB_T": 25.13,
			"VRMS_R": 222.92,
			"VRMS_S": 222.82,
			"VRMS_T": 222.93
		}
	}

	# Send Data
	Response = Test_Client.post("/", json=Data)

	# Check Response
	assert Response.status_code == 200