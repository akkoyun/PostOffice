# config.py
import multiprocessing

host = "0.0.0.0"
port = 80
workers = 2 * multiprocessing.cpu_count() + 1
log_level = "debug"
