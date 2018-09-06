#!usr/bin/python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件的绝对路径

HOST = "qdm159387494.my3w.com"
PORT = "3306"
DB = "qdm159387494_db"
USER = "qdm159387494"
PASS = "yhyj2018"
CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "THIS-A-SECRET-KEY"


