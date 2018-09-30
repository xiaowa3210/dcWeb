#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask

from app.model import config
from app.model.models import db  # 数据库

app = Flask(__name__)   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中

app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
# # 日志系统配置
# handler = logging.FileHandler('app.log', encoding='UTF-8')
# app.logger.addHandler(handler)
#from .view import projectview

#配置flask-login
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.model.models import User
from app.view.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
from app.view.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from app.view.tmp01 import tmp01 as tmp01_blueprint
app.register_blueprint(tmp01_blueprint)
from app.view.tmp05 import tmp05 as tmp05_blueprint
app.register_blueprint(tmp05_blueprint)
from app.ueditor import bp as bp_blueprint
app.register_blueprint(bp_blueprint)


from app.view.tmp03 import tmp03 as tmp03_blueprint
app.register_blueprint(tmp03_blueprint)

from app.view.back01 import back01 as back01_blueprint
app.register_blueprint(back01_blueprint)



