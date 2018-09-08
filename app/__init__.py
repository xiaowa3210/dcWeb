#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
import config  # 导入配置参数
from .models import db  # 数据库

app = Flask(__name__)   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中
db.init_app(app)

from flask_login import LoginManager
from app.models import User, db, Role, Permission
from app.view.backstage.main import main as main_blueprint
app.register_blueprint(main_blueprint)
from app.view.backstage.auth  import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# from .view import views  # 导入视图，防止末尾，避免循环导入？
# # from .view import projectview