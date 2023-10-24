# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log, Kafka
from Setup import Functions as Functions
import psutil
import time

# Services to track
Services_To_Track = ['PostOffice', 'Handler_RAW', 'Handler_Info', 'Handler_Power', 'Handler_IoT.service']

# Current Statuses
Current_Statuses = {}

# Loop Forever
while True:

    # Control for Services
    for Service in Services_To_Track:

        try:

            # Loop for Processes
            for process in psutil.process_iter(['pid', 'name']):

                # Control for Service
                if process.info['name'] == Service:

                    # Set Status
                    Status = True

                    # Break Loop
                    break

            else:

                # Set Status
                Status = False

            # Update Database
            if Service not in Current_Statuses or Current_Statuses[Service] != Status:

                # Set Current Status
                Current_Statuses[Service] = Status

                # Define DB
                DB_Module = Database.SessionLocal()

                # Record DataStream
                try:

                    # Create New Service Status Record
                    New_Service_Status = Models.Service_LOG(
                        Service = Service,
                        Service_Status = Status,
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Service_Status)

                    # Commit DataBase
                    DB_Module.commit()

                    # Log Message
                    Log.Terminal_Log("INFO", f"Status change detected for {Service}. New status: {Status}")

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding DataStream: {e}")

        except Exception as e:

            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while getting service status: {e}")

    # Her 60 saniyede bir kontrol et
    time.sleep(60)
