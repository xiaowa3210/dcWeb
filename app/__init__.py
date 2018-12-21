#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import Flask, redirect, url_for, request, session, render_template
from app.model import config
from app.model.constant import ADMIN, role_dict, TEACHER
from app.model.models import db  # 数据库
from app.model.entity import db2  # 数据库
from app.service.UserServiceV2 import UserService
from app.view.MessageInfo import MessageInfo

app = Flask(__name__, static_folder='../static', static_url_path='/static')   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中

app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
db2.init_app(app)



from app.view.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
from app.view.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from app.view.tmp01 import tmp01 as tmp01_blueprint
app.register_blueprint(tmp01_blueprint)
from app.view.tmp03 import tmp03 as tmp03_blueprint
app.register_blueprint(tmp03_blueprint)
from app.view.tmp05 import tmp05 as tmp05_blueprint
app.register_blueprint(tmp05_blueprint)

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
    #拦截需要登录才能访问的页面
    if path not in allow_url:
        if role_dict[ADMIN] in session:
            if path in disallow_url_admin:
                return redirect(url_for("login"))
        elif role_dict[TEACHER] in session:
            if path in disallow_url_teacher:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("test/login.html")

#登录功能
@app.route("/api/login",methods=['POST'])
def login_api():
    data = json.loads(request.get_data("utf-8"))
    username = data['username']
    password = data['password']
    role = data['role']
    user = userSevice.selectByName(username,role)
    if user :
        if password == user.password:
            session[role_dict[role]] = user.username             #用session保存登录状态
            resp = {
                "msg":"登录成功",
                "code":0
            }
            return json.dumps(MessageInfo.success(data=resp).__dict__)
        else:
            return json.dumps(MessageInfo.success(data="亲，密码错误!").__dict__)
    else:
        return json.dumps(MessageInfo.success(data="亲,用户不存在或选错用户类型了").__dict__)


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