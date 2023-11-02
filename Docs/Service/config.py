# config.py
import multiprocessing
from uvicorn.workers import UvicornWorker

# Custom Uvicorn Worker
class CustomUvicornWorker(UvicornWorker):

    CONFIG_KWARGS = {
        "server_header": False
    }

# Server Socket
bind = '0.0.0.0:80'

# Workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker Class
worker_class = CustomUvicornWorker()
