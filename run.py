#!usr/bin/python
# -*- coding: utf-8 -*-
from app import app
from app.utils.TimerTask import TimerTask, task

# 热更新
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

if __name__ == "__main__":
  app.run(host='0.0.0.0')
