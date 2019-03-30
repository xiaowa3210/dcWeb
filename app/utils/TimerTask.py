#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@:author:
@:file: TimerTask.py
@:time: 2019/2/16
@:descrition:定时任务类,用于每天定时执行某个任务

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import datetime
import threading


#删除获奖的excel文件
import os

from app.model.config import UPLOAD_PATH


def task():
    for filename in os.listdir(UPLOAD_PATH):
        if os.path.exists(filename):
            # 删除文件，可使用以下两种方法。
            os.remove(filename)
            # os.unlink(my_file)
class TimerTask:
    def __init__(self,task,time):
        self.task = task
        self.time = time

    """
    @:param:
    @:return:
    @descrition:启动定时任务
    """
    def start(self):
        timer = threading.Timer(self.__computeStartTime__(), self.start)
        timer.start()
        self.task()

    def __computeStartTime__(self):
        # 获取现在时间
        now_time = datetime.datetime.now()
        # 获取明天时间
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        # 获取明天3点时间
        next_time = datetime.datetime.strptime(
            str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " " + self.time, "%Y-%m-%d %H:%M:%S")

        # 获取距离明天3点时间，单位为秒
        return (next_time - now_time).total_seconds()

