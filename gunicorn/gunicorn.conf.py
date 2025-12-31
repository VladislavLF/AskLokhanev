import os
import multiprocessing


bind = f"{os.getenv('GUNICORN_HOST', '0.0.0.0')}:{os.getenv('GUNICORN_PORT', '8000')}"
workers = int(os.getenv('GUNICORN_WORKERS', 3))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
threads = int(os.getenv('GUNICORN_THREADS', 2))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 5))
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))

accesslog = os.getenv('GUNICORN_ACCESS_LOG', '/app/logs/gunicorn_access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', '/app/logs/gunicorn_error.log')
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')

reload = os.getenv('GUNICORN_RELOAD', 'false').lower() == 'true'

if os.getenv('GUNICORN_WORKERS') is None:
    workers = multiprocessing.cpu_count() * 2 + 1

capture_output = True
enable_stdio_inheritance = True
