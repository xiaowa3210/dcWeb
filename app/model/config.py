#!usr/bin/python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件的绝对路径

# 测试环境
HOST = "47.93.236.82"
PORT = "3306"
DB = "dcwebdb"
USER = "root"
PASS = "hubiao"

# 正式环境
#
# HOST = "47.107.103.134"
# PORT = "3306"
# DB = "dcwebdb"
# USER = "root"
# PASS = "Cc!12345"

# 邮件服务器配置
MAIL_SERVER = 'mail.163.com',
MAIL_PORT = '25',
MAIL_USE_SSL = False,
MAIL_USERNAME = 'hbfaker@163.com',
MAIL_PASSWORD = 'hubiao'  # （可在邮箱设置中获取）

CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "THIS-A-SECRET-KEY"

UEDITOR_UPLOAD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/'))  # 图片上传配置

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

ARTICLE_ATTACHMENT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../resources/article_attachment/'))

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static/'))

UPLOAD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/'))  # 图片上传配置

UPLOAD_PICS_PATH = os.path.abspath(os.path.join(UPLOAD_PATH, 'pics'))  # 图片上传配置

UPLOAD_FILES_PATH = os.path.abspath(os.path.join(UPLOAD_PATH, 'files'))  # 图片上传配置

UPLOAD_AWARD_PATH = os.path.abspath(os.path.join(UPLOAD_PATH, 'award'))  # 图片上传配置

UPLOAD_ZIP_PATH = os.path.abspath(os.path.join(UPLOAD_PATH, 'zip'))  # zip上传配置


# 系统中有三种用户,学生,管理员,超级管理员,需要登录允许访问的URL


allow_url = [
    '/'
]


stu_allow_url = [
    '/api/addPro',
    '/api/addProMember',
    '/api/addProAward',
    '/api/modifyPro',
    '/api/modifyProMember',
    '/api/modifyProAward',
    '/api/modifyMainPic',
    '/api/modifyMainPic',
    '/api/deleteProMember',
    '/api/deleteProAward',
    '/api/uploadProject',
    '/api/downloadAwardInfo',
    '/api/uploadProjectV2',
    '/api/student/deletePro',
    '/student/manageProject',
    '/student/modifiesProject',
    '/student/uploadProject',
    '/student/preview/project'
]

common_admin_allow_url = [
    '/admin/main',
    '/api/admin/deleteNew',
    '/api/admin/addNew',
    '/admin/modifiesNews',
    '/adminNews'
]

admin_allow_url = [
    # '/api/admin/addNew',
    # '/admin/modifiesNews',
    # '/adminNews'
]

superadmin_allow_url = [
    '/admin/manageNews',
    '/admin/manageResource',
    '/admin/editFiles',
    '/admin/manageUser',
    '/admin/checkNewView',
    '/api/admin/uploadFile',
    '/api/admin/deleteFile',
    '/api/admin/deletePro',
    '/api/admin/undoPro',
    '/api/admin/checkoutPro',
    '/api/admin/downAwardInfo',
    '/admin/checkproject',
    '/admin/checkProjects',
    '/admin/manageProject',
    '/admin/deleteProject',
    '/admin/manageResource',
    '/admin/editFiles',
    '/admin/manageUser'
]
