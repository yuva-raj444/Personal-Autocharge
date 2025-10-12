# Gunicorn configuration for Render deployment
# This file configures gunicorn to handle long-running automation tasks

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 2048

# Worker processes
workers = 1  # Single worker to avoid resource conflicts
worker_class = "sync"
worker_connections = 1000
timeout = 120  # 2 minutes timeout for automation tasks
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 100
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "jio-recharge-automation"

# Preload app for better memory usage
preload_app = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Enable thread support
threads = 2

# Graceful timeout
graceful_timeout = 30

def when_ready(server):
    server.log.info("🚀 Jio Recharge Automation Server is ready to accept connections")

def worker_int(worker):
    worker.log.info(f"⚠️  Worker {worker.pid} received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info(f"🔧 Worker {worker.pid} spawned")

def post_fork(server, worker):
    server.log.info(f"✅ Worker {worker.pid} ready")

def worker_abort(worker):
    worker.log.error(f"❌ Worker {worker.pid} aborted")