bind = "127.0.0.1:18650"
pidfile = "./run/gunicorn.pid"
logfile = "./run/gunicorn.log"
loglevel = "info"
workers = 2
timeout = graceful_timeout = 60
