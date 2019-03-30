#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import Flask, redirect, url_for, request, session, render_template
from dcwebapp.model import config
from dcwebapp.model.constant import ADMIN, role_dict, TEACHER
from dcwebapp.model.models import db  # 数据库
from dcwebapp.model.entity import db2  # 数据库
from dcwebapp.service.UserServiceV2 import UserService
from dcwebapp.view.MessageInfo import MessageInfo
from flask_mail import Mail

mail = Mail()
app = Flask(__name__, static_folder='../static', static_url_path='/static')   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中

app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
db2.init_app(app)
mail.init_app(app)



from dcwebapp.view.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
from dcwebapp.view.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from dcwebapp.view.tmp01 import tmp01 as tmp01_blueprint
app.register_blueprint(tmp01_blueprint)
from dcwebapp.view.tmp03 import tmp03 as tmp03_blueprint
app.register_blueprint(tmp03_blueprint)
from dcwebapp.view.tmp05 import tmp05 as tmp05_blueprint
app.register_blueprint(tmp05_blueprint)


from dcwebapp.view.front import front as front_blueprint
app.register_blueprint(front_blueprint)
from dcwebapp.view.common import common as common_blueprint
app.register_blueprint(common_blueprint)
from dcwebapp.view.back import back as back_blueprint
app.register_blueprint(back_blueprint)


userSevice = UserService()
#不需要拦截的url
allow_url = [
    "/login"
]

#管理员不允许访问的url
disallow_url_admin = [

]

# 老师不允许访问的url
disallow_url_teacher = [

]

#登录验证
@app.before_request
def before_action():
    path = request.path
    #拦截url中带admin的请求,做登录验证
    if 'admin' in path:
        if 'admin' not in session:
            return redirect(url_for('back.login'))




# # 日志系统配置
# handler = logging.FileHandler('app.log', encoding='UTF-8')
# app.logger.addHandler(handler)
#from .view import projectview

# #配置flask-login
# from flask_login import LoginManager
# login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'auth.login'
# login_manager.login_message = '请先登录'
# login_manager.init_app(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# from app.model.models import User

# '''ueditor配置接口'''
# #from app.ueditor import bp as bp_blueprint
# #app.register_blueprint(bp_blueprint)
# from app.view.ueditor import ueditor#editor后台配置接口，用于获取配置
# app.register_blueprint(ueditor)
# from app.view.back01 import back01#back01注册蓝图
# app.register_blueprint(back01, url_prefix='/back01')
# from app.view.API import api#api接口
# app.register_blueprint(api, url_prefix='/api')
