#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import Flask, redirect, url_for, request, session, render_template
from app.model import config
from app.model.config import superadmin_allow_url, admin_allow_url, stu_allow_url, common_admin_allow_url, allow_url
from app.model.constant import ADMIN, role_dict, TEACHER
from app.model.entity import db2  # 数据库
from app.service.UserServiceV2 import UserService
from app.view.MessageInfo import MessageInfo
from flask_mail import Mail

mail = Mail()
app = Flask(__name__, static_folder='../static', static_url_path='/static')   # 新建一个flask应用
app.config.from_object(config)  # 将配置文件导入应用中

app.config["SQLALCHEMY_ECHO"] = True

db2.init_app(app)
mail.init_app(app)




from app.view.front import front as front_blueprint
app.register_blueprint(front_blueprint)
from app.view.common import common as common_blueprint
app.register_blueprint(common_blueprint)
from app.view.back import back as back_blueprint
app.register_blueprint(back_blueprint)


userSevice = UserService()
# #不需要拦截的url
# allow_url = [
#     "/login"
# ]
#
# #管理员不允许访问的url
# disallow_url_admin = [
#
# ]
#
# # 老师不允许访问的url
# disallow_url_teacher = [
#
# ]
#
# # 老师不允许访问的url
# allow_url_student = [
#     '/user'
# ]


def isContain(url,urls):
    for u in urls:
        if url in u: return True
    return False

#登录验证
@app.before_request
def before_action():
    path = request.path
    #拦截url中带admin的请求,做登录验证

    if not isContain(path,allow_url):
        if isContain(path, stu_allow_url):
            if 'student' not in session:
                return redirect(url_for('front.stu_login'))
        if isContain(path, common_admin_allow_url):
            if 'admin' not in session:
                return redirect(url_for('back.login'))
        if isContain(path, admin_allow_url):
            if 'admin' not in session or session['admin']['type'] == 0:
                return redirect(url_for('back.login'))
        if isContain(path, superadmin_allow_url):
            if 'admin' not in session or session['admin']['type'] == 2:
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
# from app.view.back import back#back注册蓝图
# app.register_blueprint(back, url_prefix='/back')
# from app.view.API import api#api接口
# app.register_blueprint(api, url_prefix='/api')
