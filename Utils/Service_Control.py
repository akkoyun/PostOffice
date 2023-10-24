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
            Status = False
            try:
                if Service in all_processes:
                    Log.Terminal_Log("INFO", f"Checking {Service} - {all_processes[Service]}")
                    Status = True
                
                # Update database only if status has changed
                if Service not in Current_Statuses or Current_Statuses[Service] != Status:
                    Current_Statuses[Service] = Status

                    try:
                        DB_Module = Database.SessionLocal()
                        New_Service_Status = Models.Service_LOG(
                            Service=Service,
                            Service_Status=Status,
                        )
                        DB_Module.add(New_Service_Status)
                        DB_Module.commit()
                        Log.Terminal_Log("INFO", f"Status change detected for {Service}. New status: {Status}")

                    except SQLAlchemyError as db_err:
                        Log.Terminal_Log("ERROR", f"Database Error: {db_err}")
                    finally:
                        DB_Module.close()

            except Exception as e:
                Log.Terminal_Log("ERROR", f"An error occurred while processing service {Service}: {type(e).__name__} - {e}")

    except Exception as e:
        Log.Terminal_Log("ERROR", f"An unexpected error occurred: {type(e).__name__} - {e}")

    time.sleep(60)