#!/usr/bin/env bash

case $1 in
  "start")
    echo "start service"
    nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app&
  ;;
  "stop")
    echo "stop service"
    pkill gunicorn
  ;;
  "restart")
    echo "restart service"
    pkill gunicorn & nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app&
  ;;
  *)
    echo "parameter error!!parameter(start|stop|restart)"
    ;;
esac