#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import create_app
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# from dcWeb_2_0.app import db
# from app import models
# from.app.newmodels import SuperAdmin
from flask_uploads import configure_uploads, patch_request_class

from backapp.backstage import create_app,login_manager
# app = Flask(__name__)
from backapp.backstage.main.forms import photos

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# db = SQLAlchemy(app)

# db.init_app(app)
app.config['SECRET_KEY'] = 'THIS-A-SECRET-KEY'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/demo1'  # 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hubiao@47.93.236.82:3306/dachuang'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
# configure_uploads(app, photos)
# 配置上传文件大小，默认64M，设置None则会采用MAX_CONTENT_LENGTH配置选项
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
# patch_request_class(app, size=None)

# login_manger = LoginManager()
# login_manger.session_protection = 'strong'
# login_manger.login_view = 'auth.login'
# login_manger.init_app(app)
#
# login_manger.init_app(app)
#
# from backapp.backstage.main import main as main_blueprint
# app.register_blueprint(main_blueprint)
#
# from backapp.backstage.auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)
from app.models import db
db.init_app(app)
db.app=app
with app.test_request_context():
    from app.models import *
    # db.drop_all()
    db.create_all()
from app.models import SuperAdmin
admin = SuperAdmin(username='admin',password='admin')
db.session.add(admin)
db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return SuperAdmin.query.get(int(user_id))



if __name__ == '__main__':
    app.run(debug=True)
