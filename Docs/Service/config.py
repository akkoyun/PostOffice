# config.py
import multiprocessing

# Server Socket
bind = '0.0.0.0:80'

# Workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker Class
worker_class = 'uvicorn.workers.UvicornWorker'
