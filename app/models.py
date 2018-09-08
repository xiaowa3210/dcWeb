
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

    def get_id(self):
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

#角色表
class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleName = db.Column(db.String(64),index=True,unique=True,nullable=False)
    users = db.relationship('User',
                         secondary = user_role,
                         back_populates='roles')
    def __init__(self,rolename):
        self.roleName = rolename
    permissions = db.relationship('Permission',
                         secondary = role_permission,
                         back_populates='roles')

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

#文档表（包括新闻公告和资料下载）
class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.TEXT, nullable=True)
    type = db.Column(db.Integer,nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    attachments = db.relationship('Attachment', back_populates='document')

#附件表
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(256), nullable=False)
    documentId = db.Column(db.Integer, ForeignKey('document.id'))

    document = db.relationship('Document',back_populates="attachments")

#项目表
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pname = db.Column(db.String(256), nullable=False)
    users = db.relationship('User',
                         secondary=user_project,
                         back_populates='projects')

    introduction = db.Column(db.TEXT, nullable=False)
    picture = db.Column(db.String(1024), nullable=True)
    vedio = db.Column(db.String(1024), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    def __repr__(self):
        return "<Project(id='%s',pname='%s',team_info='%s',introduction='%s',picture='%s',vedio='%s',create_time='%s')>" % \
               (self.id,self.pname,self.team_info,self.introduction,self.picture,self.vedio,self.create_time)






