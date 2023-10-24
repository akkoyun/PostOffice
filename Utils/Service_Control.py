import sys
import time
import psutil

sys.path.append('/root/PostOffice/')

from Setup import Database, Models, Log, Kafka
from Setup import Functions as Functions

Services_To_Track = ['PostOffice', 'Handler_RAW', 'Handler_Info', 'Handler_Power', 'Handler_IoT.service']
Current_Statuses = {}

while True:
    for Service in Services_To_Track:
        try:
            Status = False
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                process_name = process.info['name']
                process_cmdline = ' '.join(process.info.get('cmdline', []))

                # Burada hem işlemin adını hem de komut satırı argümanlarını kontrol ediyoruz.
                if process_name == Service or Service in process_cmdline:
                    Status = True
                    Log.Terminal_Log("INFO", f"Checking {process_name} - {process.info['pid']}")
                    break

            if Service not in Current_Statuses or Current_Statuses[Service] != Status:
                Current_Statuses[Service] = Status

                DB_Module = Database.SessionLocal()
                try:
                    New_Service_Status = Models.Service_LOG(
                        Service=Service,
                        Service_Status=Status,
                    )
                    DB_Module.add(New_Service_Status)
                    DB_Module.commit()
                    Log.Terminal_Log("INFO", f"Status change detected for {Service}. New status: {Status}")

                except Exception as e:
                    Log.Terminal_Log("ERROR", f"An error occurred while adding DataStream: {e}")

        except Exception as e:
            Log.Terminal_Log("ERROR", f"An error occurred while getting service status: {e}")

    time.sleep(60)
