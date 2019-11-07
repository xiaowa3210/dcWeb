#!usr/bin/python
# -*- coding: utf-8 -*-
from app import app
from app.utils.TimerTask import TimerTask, task

if __name__ == "__main__":
  app.run(host='0.0.0.0')

  # #启动一个定时器每天凌晨1点删除excel表
  # TimerTask(task(),"01:00:00").start()
