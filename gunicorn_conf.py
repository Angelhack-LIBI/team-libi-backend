import os

loglevel = os.getenv('LOG_LEVEL', 'info')
workers = int(os.environ['WORKERS']) if os.getenv('WORKERS', '').isdigit() else 1
bind = os.getenv('BIND', None) or '0.0.0.0:80'
errorlog = os.getenv('ERROR_LOG', '-') or None
worker_tmp_dir = '/dev/shm'
accesslog = os.getenv('ACCESS_LOG', '-') or None
graceful_timeout = int(os.getenv('GRACEFUL_TIMEOUT', 120))
timeout = int(os.getenv('TIMEOUT', 120))
keepalive = int(os.getenv('KEEP_ALIVE', 5))
