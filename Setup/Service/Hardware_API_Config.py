# config.py
import multiprocessing
from uvicorn.workers import UvicornWorker

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
bind = '0.0.0.0:4862'

# Workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker Class
worker_class = 'Setup.Service.Hardware_API_Config.CustomUvicornWorker'

# Worker Timeout
worker_timeout = 60

# Worker Max Requests
max_requests = 1000

# Worker Max Requests Jitter
max_requests_jitter = 100

# Error Log
errorlog = '/root/PostOffice/Log/Hardware_API_Error.LOG'

# Access Log
accesslog = '/root/PostOffice/Log/Hardware_API_Access.LOG'