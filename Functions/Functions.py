# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models

# Get Service Status
def Get_Service_Status(Service: str):

    # Define Status
    Service_State = False

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Control Service
        Query_Status = (DB_Module.query(Models.Service_LOG).filter(Models.Service_LOG.Service.like(Service)).order_by(Models.Service_LOG.Update_Time.desc()).first())

        # Service Found
        if Query_Status is not None:

            # Return Service State
            Service_State = Query_Status.Status

    finally:
        
        # Close Database
        DB_Module.close()

    # Return Status
    return Service_State
