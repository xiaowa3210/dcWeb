
import os
basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件的绝对路径

HOST = "47.93.236.82"
PORT = "3306"
DB = "dcwebdb"
USER = "root"
PASS = "hubiao"
CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "THIS-A-SECRET-KEY"
