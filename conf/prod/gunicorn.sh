#!/bin/bash
set -e
APP_NAME=Gosocket_API

# user/group to run as
USER=ubuntu
GROUP=ubuntu

LOGFILE=/home/$USER/logs/$APP_NAME/gunicorn.log
LOGDIR=$(dirname $LOGFILE)

cd /home/ubuntu/src/Gosocket_API
source /home/ubuntu/venvs/Gosocket_API/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR

exec /home/ubuntu/venvs/Gosocket_API/bin/gunicorn -c /home/ubuntu/src/Gosocket_API/conf/prod/gunicorn.conf \
--user=$USER --group=$GROUP --log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE Gosocket.wsgi
