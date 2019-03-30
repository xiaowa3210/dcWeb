#!usr/bin/python
# -*- coding: utf-8 -*-
from app import app
from app.utils.TimerTask import TimerTask, task

if __name__ == "__main__":
  app.run(host='0.0.0.0')
