import sys
import time
import psutil
from sqlalchemy.exc import SQLAlchemyError  # Or your specific DB API's error

sys.path.append('/root/PostOffice/')
from Setup import Database, Models, Log, Kafka
from Setup import Functions as Functions

Services_To_Track = ['PostOffice', 'Handler_RAW', 'Handler_Info', 'Handler_Power', 'Handler_IoT.service']
Current_Statuses = {}

while True:
    try:
        # Here, instead of getting processes for each service, we get them all at once.
        all_processes = {p.info['name']: p.info['pid'] for p in psutil.process_iter(['pid', 'name'])}

        for Service in Services_To_Track:

            for process in psutil.process_iter(['pid', 'name']):
                print(process.info)



    except Exception as e:
        Log.Terminal_Log("ERROR", f"An unexpected error occurred: {type(e).__name__} - {e}")

    time.sleep(60)