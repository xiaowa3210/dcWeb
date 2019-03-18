#!usr/bin/python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime

db2 = SQLAlchemy()
# 用户表
class User(db2.Model):
    __tablename__ = 'dc_user'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    username = db2.Column(db2.String(64), index=True, unique=True, nullable=False)
    nickname = db2.Column(db2.String(64), nullable=True)
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
#项目表
class Project(db2.Model):
    __tablename__ = 'dc_project'
    pid = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    pname = db2.Column(db2.String(256), nullable=False)                             #项目名
    content = db2.Column(db2.TEXT,nullable=False)                                   #项目内容
    src_content = db2.Column(db2.TEXT,nullable=False)                                   #项目内容
    type = db2.Column(db2.String(256), nullable=False)                                  #项目类别
    mainPic = db2.Column(db2.String(256),nullable=True)                             #主页图片
    members = db2.relationship('ProjectMember',backref='project',lazy='dynamic')
    status = db2.relationship('ProjectStatus',uselist=False,backref='project')
    awards = db2.relationship('ProjectAward',backref='project',lazy='dynamic')

    def __init__(self,pname,content,type):
        self.pname = pname
        self.content = content
        self.type = type
#项目状态表
class ProjectStatus(db2.Model):
    __tablename__ = 'dc_project_status_info'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    pid = db2.Column(db2.Integer, db2.ForeignKey('dc_project.pid'))                 #外键关联dc_project表，一对一关系
    pname = db2.Column(db2.String(256),nullable=False)                              #项目名
    type = db2.Column(db2.Integer, nullable=False)                                  #项目类别
    publisher = db2.Column(db2.String(256), nullable=False)                         #上传者
    reviewer = db2.Column(db2.String(256), nullable=True)                           #审核人
    undoer = db2.Column(db2.String(256), nullable=True)                             #撤销人
    status = db2.Column(db2.Integer, nullable=False)                                #状态
    createTime = db2.Column(DateTime, nullable=False, default=datetime.now)         #创建时间
    modifiedTime = db2.Column(DateTime, nullable=True)                              #修改时间
    cancelTime = db2.Column(DateTime, nullable=True)                                #撤销时间
    submitTime = db2.Column(DateTime, nullable=True)                                #提交时间
    checkTime = db2.Column(DateTime, nullable=True)                                 #审核时间
    msg = db2.Column(db2.TEXT, nullable=True)                                       #审核所附加的信息
    delete_flag = db2.Column(db2.DECIMAL(1, 0), nullable=False, default=0)          #删除标志
    mainPic = db2.Column(db2.String(256), nullable=True)                            # 主页图片


    def __init__(self,pname,type,publisher,status):
        self.pname = pname
        self.type = type
        self.publisher = publisher
        self.status = status
#项目成员表
class ProjectMember(db2.Model):
    __tablename__ = 'dc_project_member'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    pid = db2.Column(db2.Integer, db2.ForeignKey('dc_project.pid'))                 #外键关联dc_project表，多对一关系
    name = db2.Column(db2.String(32),nullable=False)                                #姓名
    academy = db2.Column(db2.String(128),nullable=True)                             #学院
    grade = db2.Column(db2.String(128),nullable=True)                               #年级
    type = db2.Column(db2.String(128), nullable=False)                                  #类型
    brief = db2.Column(db2.TEXT, nullable=True)                                     #简介

    def __init__(self,name,type):
        self.name = name
        self.type = type
#项目奖项表
class ProjectAward(db2.Model):
    __tablename__ = 'dc_project_award'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    awardName = db2.Column(db2.String(128),nullable=False)                          # 获奖名
    certPic = db2.Column(db2.TEXT,nullable=True)                                    # 证书扫描件地址
    honorLink = db2.Column(db2.String(128),nullable=True)                           # 获奖链接
    awardTime = db2.Column(DateTime, nullable=True)                                 # 获奖时间
    pid = db2.Column(db2.Integer, db2.ForeignKey('dc_project.pid'))                 # 外键关联dc_project表，多对一关系

    def __init__(self,awardName):
        self.awardName = awardName

#新闻表
class New(db2.Model):
    __tablename__ = 'dc_new'
    nid = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    title = db2.Column(db2.String(256),nullable=False)                        #标题
    content = db2.Column(db2.TEXT, nullable=True)                             #html内容
    src_content = db2.Column(db2.TEXT, nullable=True)                         #markdown内容
    extInfo = db2.relationship('newExt', uselist=False, backref='new')
    def __init__(self,title,content,src_content):
        self.title = title
        self.content = content
        self.src_content = src_content
#新闻额外信息表 
class newExt(db2.Model):
    __tablename__ = 'dc_new_ext'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    nid = db2.Column(db2.Integer, db2.ForeignKey('dc_new.nid'))               # 外键关联dc_new表
    title = db2.Column(db2.String(256), nullable=False)                       # 新闻标题
    status = db2.Column(db2.Integer, nullable=False)                          # 状态：0代表未发布,1代表已发布
    creater = db2.Column(db2.String(256), nullable=False)                     # 创建人
    publisher = db2.Column(db2.String(256), nullable=True)                   # 发布人
    modifier = db2.Column(db2.String(256), nullable=False)                    # 最后修改人
    createTime = db2.Column(DateTime, nullable=False, default=datetime.now)   # 创建时间
    modifiedTime = db2.Column(DateTime, nullable=True)                        # 最后修改时间
    cancelTime = db2.Column(DateTime, nullable=True)                          # 撤销时间
    submitTime = db2.Column(DateTime, nullable=True)                          # 提交时间
    publisherTime = db2.Column(DateTime, nullable=True)                       # 发布时间
    deleteFlag = db2.Column(db2.DECIMAL(1, 0), nullable=False, default=0)     # 发布时间


    def __init__(self,title,status):
        self.title = title
        self.status = status
#附件表
class Files(db2.Model):
    __tablename__ = 'dc_files'
    fid = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    name = db2.Column(db2.String(256),nullable=False)
    path = db2.Column(db2.String(128),nullable=False)
    source = db2.Column(db2.Integer,nullable=False)#1:代表资料下载文件。2:代表新闻附件。3:代表项目附件
    source_id = db2.Column(db2.Integer,nullable=True)
    delete_flag = db2.Column(db2.DECIMAL(1,0),nullable=False,default=0)
