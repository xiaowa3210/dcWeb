#!usr/bin/python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

db2 = SQLAlchemy()
# 用户表
class User(db2.Model):
    __tablename__ = 't_user'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    username = db2.Column(db2.String(64), index=True, unique=True, nullable=False)
    password = db2.Column(db2.String(128), nullable=False)
    type = db2.Column(db2.Integer, nullable=False)
    created_time = db2.Column(DateTime, nullable=True, default=datetime.now)
    modified_time = db2.Column(DateTime, nullable=True)

    def __init__(self, username, pwd, type):
        self.username = username
        self.password = pwd
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.username
