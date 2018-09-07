#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging

from flask import Flask
import config  # 导入配置参数
from .models import db  # 数据库

app = Flask(__name__)   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中
db.init_app(app)

# # 日志系统配置
# handler = logging.FileHandler('app.log', encoding='UTF-8')
# app.logger.addHandler(handler)

from .view import projectview