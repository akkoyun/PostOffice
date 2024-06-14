# config.py
import multiprocessing
from uvicorn.workers import UvicornWorker
from Setup.Config import APP_Settings

# Custom Uvicorn Worker
class CustomUvicornWorker(UvicornWorker):

    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "lifespan": "on",
        "server_header": False,
        "date_header": False,
    }

# Server Socket
bind = '0.0.0.0:8000'

# Workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker Class
worker_class = 'Docs.Service.PostOffice_config.CustomUvicornWorker'

# Worker Timeout
worker_timeout = 120

# Worker Graceful Timeout
graceful_timeout = 120

# Worker Max Requests
max_requests = 1000

# Worker Max Requests Jitter
max_requests_jitter = 100

# Error Log
errorlog = str(APP_Settings.LOG_SERVICE_ERROR)

# Access Log
accesslog = str(APP_Settings.LOG_SERVICE_ACCESS)