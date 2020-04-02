#!/bin/bash

NAME="mass_mailer_server"                                  # Name of the application
VIRTUALENV=/home/ubuntu/mass_mailer/venv/bin/             # Django project directory
PROJ_DIRECTORY=/home/ubuntu/mass_mailer/             # Django project directory
SOCKFILE=/home/ubuntu/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                        # the user to run as
GROUP=ubuntu                                     # the group to run as
NUM_WORKERS=5                                     # how many worker processes should Gunicorn spawn
MAX_REQUEST=100                                 # how many requests before restarting
#WORKER_CLASS=gevent
TIMEOUT=1000
ERROR_LOG_FILE=/home/ubuntu/logs/gunicorn_error.log
DJANGO_SETTINGS_MODULE=project.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=project.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $VIRTUALENV
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$PROJ_DIRECTORY:$PYTHONPATH

# Environment variable
export LSS_ENV=prod

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/ubuntu/mass_mailer/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --max-requests $MAX_REQUEST \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=error \
  --log-file=$ERROR_LOG_FILE
