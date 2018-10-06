#!usr/bin/python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime

db = SQLAlchemy()

#用户角色关联
user_role = db.Table('t_user_role',
                  db.Column('userId', db.Integer,ForeignKey('t_user.id'), primary_key=True),
                  db.Column('roleId', db.Integer,ForeignKey('t_role.id'), primary_key=True))

#项目用户表关联表
user_project = db.Table('t_user_project',
                  db.Column('userId', db.Integer,ForeignKey('t_user.id'), primary_key=True),
                  db.Column('projectId', db.Integer,ForeignKey('project.id'), primary_key=True))

#角色权限关联表
role_permission = db.Table('t_role_permission',
                  db.Column('roleId', db.Integer,ForeignKey('t_role.id'), primary_key=True),
                  db.Column('permissionId', db.Integer,ForeignKey('t_permission.id'), primary_key=True))


#用户表
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(64),index=True,unique=True,nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_time = db.Column(DateTime, nullable=True, default=datetime.now)

    roles = db.relationship('Role',
                         secondary = user_role,
                         back_populates='users')

    projects = db.relationship('Project',
                         secondary=user_project,
                         back_populates='users')

    modified_time = db.Column(DateTime, nullable=True, default=datetime.now)


    def __init__(self, username, pwd):
        self.username = username
        self.password = pwd

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
            return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


#角色表
class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleName = db.Column(db.String(64),index=True,unique=True,nullable=False)
    users = db.relationship('User',
                         secondary = user_role,
                         back_populates='roles')
    permissions = db.relationship('Permission',
                         secondary = role_permission,
                         back_populates='roles')
    def __init__(self, rolename):
        self.roleName = rolename

#权限表
class Permission(db.Model):
    __tablename__ = 't_permission'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permissionName = db.Column(db.String(64), nullable=False)
    permissionLabel = db.Column(db.String(64), nullable=False)
    
    roles = db.relationship('Role',
                         secondary = role_permission,
                         back_populates='permissions')


    def __init__(self, permissionName,permissionLabel):
        self.permissionName = permissionName
        self.permissionLabel = permissionLabel





# 文档表（包括新闻公告和资料下载）
class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.TEXT, nullable=True)
    type = db.Column(db.Integer, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    attachments = db.relationship('Attachment', back_populates='document')


# 附件表
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(256), nullable=False)
    documentId = db.Column(db.Integer, ForeignKey('document.id'))
    document = db.relationship('Document', back_populates="attachments")


# 项目表
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pname = db.Column(db.String(256), nullable=False)
    users = db.relationship('User',
                         secondary=user_project,
                         back_populates='projects')
    introduction = db.Column(db.TEXT, nullable=False)
    #队伍信息
    teaminfo = db.Column(db.TEXT,nullable=True)
    picture = db.Column(db.String(1024), nullable=True)
    vedio = db.Column(db.String(1024), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return "<Project(id='%s',pname='%s',users='%s',introduction='%s',picture='%s',vedio='%s',create_time='%s')>" % \
               (self.id,self.pname,self.users,self.introduction,self.picture,self.vedio,self.create_time)


#实验室介绍
class Laboratory(db.Model):
    __tablename__ = 'laboratory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    introduction = db.Column(db.TEXT, nullable=False)
    activities = db.relationship('Activity', back_populates='laboratory')
    member = db.Column(db.String(256),nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_json(self):
        json_lab = {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'activities': self.activities,
            'member': self.member,
            'create_time': self.create_time
        }

        return json_lab

#实验室活动介绍(考虑富文本)
class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = name = db.Column(db.String(256), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    lid = db.Column(db.Integer, ForeignKey(Laboratory.id))
    laboratory = db.relationship('Laboratory', back_populates='activities')




#文稿类
class Article(db.Model):
    __tablename__ = 't_article'

    article_id = db.Column(db.String(30), primary_key=True)

    #'稿件类型：1图文，2图集，3视频，4外部稿件（录入url）, 5音频,6VR视频'
    article_type = db.Column(db.DECIMAL(2,0), nullable=False)

    #标题
    title = db.Column(db.String(256), nullable=True)

    #副标题
    sub_title = db.Column(db.String(256), nullable=True)

    #标题颜色
    title_color = db.Column(db.String(20), nullable=True,default="black")

    #摘要
    brief = db.Column(db.TEXT, nullable=True)

    #关键字
    key_words = db.Column(db.String(256), nullable=True)

    #来源ID
    source_id = db.Column(db.String(30),nullable=True)

    #权重
    weight = db.Column(db.DECIMAL(3,0),nullable=True)

    #内容
    content = db.Column(db.Text(length=(2**32)-1),nullable=True)

    #创建人ID
    creator_id = db.Column(db.String(30),nullable=False)


    #创建时间
    create_time = db.Column(db.DateTime, nullable=False,default=datetime.now)

    #发布标志,0未发布，1已发布,2已发布正编辑
    publish_sign = db.Column(db.DECIMAL(1,0), nullable=False, default=0)

    #发布人ID
    publish_id = db.Column(db.String(30),nullable=True)

    #发布时间
    publish_time = db.Column(db.DateTime, nullable=True)

    #最后修改人ID
    last_modified_id = db.Column(db.String(30),nullable=True)

    #最后修改时间
    last_modified_time = db.Column(db.DateTime, nullable=True)

    #是否有附件,0代表有，1代表没有
    is_attachment = db.Column(db.DECIMAL(1,0),nullable=False)

    #标签
    tags = db.Column(db.String(256),nullable=True)

    #删除标志：0未删除，1已删除
    delete_flag = db.Column(db.DECIMAL(1,0),nullable=False,default=0)

    #删除人ID
    deleter_id = db.Column(db.String(30),nullable=True)

    # 删除时间
    delete_time = db.Column(db.DateTime, nullable=True)

    #真实发布时间
    true_publish_time = db.Column(db.DateTime, nullable=True)


    files = db.relationship('Files', back_populates='article')

#附件类
class Files(db.Model):
    __tablename__ = 't_files'

    #稿件附件id
    file_id = db.Column(db.String(30), primary_key=True)

    #'稿件id
    article_id = db.Column(db.String(30), ForeignKey('t_article.article_id'))

    article = db.relationship('Article', back_populates='files')

    #类型
    type  = db.Column(db.DECIMAL(2,0), nullable=True)

    #图片附属信息
    img_info = db.Column(db.String(256), nullable=True)

    #序号
    sn = db.Column(db.DECIMAL(5,0), nullable=True)

    #外网url
    url = db.Column(db.String(256), nullable=True)

    #本地绝对路径
    local_path = db.Column(db.String(256), nullable=True)

    #本地文件名
    local_name = db.Column(db.String(256), nullable=True)

    #本地预览url
    local_url = db.Column(db.String(256), nullable=True)

    #发布标志：0未发布，1 已发布
    publish_flag = db.Column(db.DECIMAL(1,0), nullable=True)

    #标题
    title = db.Column(db.String(256), nullable=True)

    #简介
    brief = db.Column(db.String(256), nullable=True)

class nProject(db.Model):
    __tablename__ = 't_project'

    # 项目ID
    project_id = db.Column(db.String(30), primary_key=True)

    #项目名称
    title = db.Column(db.String(256), nullable=True)

    #项目简介
    brief = db.Column(db.String(1024), nullable=True)

    #项目建立时间
    broad_time = db.Column(db.DateTime, nullable=False)

    #项目宣传多图，相对路径，json串方式存储
    ban_url = db.Column(db.String(512), nullable=True)

    #删除标志：0未删除，1已删除
    delete_flag = db.Column(db.DECIMAL(1,0), nullable=False)

    #发布标志：0未发布，1已发布
    publish_flag = db.Column(db.DECIMAL(1, 0), nullable=False)

    #修改标志：0未修改，1已修改
    modified_flag = db.Column(db.DECIMAL(1, 0), nullable=False)

    # 创建人ID
    creator_id = db.Column(db.String(30), nullable=False)

    #指导老师ID
    manager_id = db.Column(db.String(30), nullable=True)

    #成员信息
    member_info = db.Column(db.String(1024), nullable=True)

    # 创建时间
    create_time = db.Column(db.DateTime, nullable=False)

    # 发布时间
    publish_time = db.Column(db.DateTime, nullable=True)

    # 关键字
    key_worlds = db.Column(db.String(256), nullable=True)

