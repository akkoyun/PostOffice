# Importing required modules
import sys
import time
import psutil

# Adding PostOffice to sys.path
sys.path.append('/root/PostOffice/')

# Importing required modules
from Setup import Database, Models, Log, Kafka
from Setup import Functions as Functions

# Define Services to Track
Services_To_Track = ['PostOffice', 'Handler_RAW', 'Handler_Device', 'Handler_WeatherStat']

# Define Current Statuses
Current_Statuses = {}

# Start Tracking
while True:

    # Check Services
    for Service in Services_To_Track:

        try:

            # Define Status
            Status = False

            # Get Processes
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                
                # Get Process Info
                process_name = process.info['name']
                
                # Get Process Command Line
                process_cmdline = ' '.join(process.info.get('cmdline', []))

                # Check if Service is Running
                if process_name == Service or Service in process_cmdline:
                    
                    # Set Status
                    Status = True

                    # Break Loop
                    break

            # Check if Status Changed
            if Service not in Current_Statuses or Current_Statuses[Service] != Status:
                
                # Set Current Status
                Current_Statuses[Service] = Status

                # Define DB
                DB_Module = Database.SessionLocal()
                
                # Add New Service Status
                try:
                    
                    # Create New Service Status
                    New_Service_Status = Models.Service_LOG(
                        Service=Service,
                        Service_Status=Status,
                    )

                    # Add Record to DataBase
                    DB_Module.add(New_Service_Status)
                    
                    # Commit DataBase
                    DB_Module.commit()
                    
                    # Log Message
                    Log.Terminal_Log("INFO", f"Status change detected for {Service}. New status: {Status}")

                # Rollback DataBase
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding DataStream: {e}")

        # Rollback DataBase
        except Exception as e:
            
            # Log Message
            Log.Terminal_Log("ERROR", f"An error occurred while getting service status: {e}")

    # Wait 60 seconds
    time.sleep(60)
