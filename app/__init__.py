#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
import config  # 导入配置参数
from .models import db  # 数据库

app = Flask(__name__)   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中
db.init_app(app)
#with app.test_request_context():
 #   db.drop_all()
 #   db.create_all()  # 创建数据表

from .view import views  # 导入视图，防止末尾，避免循环导入？
