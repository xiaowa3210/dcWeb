#!usr/bin/python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件的绝对路径



#测试环境

HOST = "47.93.236.82"
PORT = "3306"
DB = "dcwebdb"
USER = "root"
PASS = "hubiao"


#正式环境
'''
HOST = "47.107.103.134"
PORT = "3306"
DB = "dcwebdb"
USER = "root"
PASS = "Cc!12345"

'''

CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "THIS-A-SECRET-KEY"

UEDITOR_UPLOAD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../files/')) #图片上传配置

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

ARTICLE_ATTACHMENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../files/article_attachment/'))


STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static/'))
