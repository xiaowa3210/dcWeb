#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:
@file: UserServiceV2.py
@time: 2018/12/20
@descrition:用户业务类

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from app.model.entity import User
from app import db2
from app.model.constant import *
class UserService:

    """
    添加用户
    """
    def addUser_v1(self,user):
        db2.session.add(user)
        db2.session.commit()


    """ 
    修改密码
    """
    def modifiedPw(self,uid, newPw):
        params = {
            "password": newPw,
            "uid": uid
        }
        sql = 'update t_user set password=(:password) WHERE id=(:uid)'
        db2.session.execute(sql, params)
        db2.session.commit()

    """ 
    根据username前缀模糊查询记录
    """
    def selectByNamePerfix(self,name):
        return db2.session.query(User).filter(User.username.like(name + '%'))

    """ 
    根据username和类型查询记录
    """
    def selectByName(self,name,type):
        try:
            return db2.session.query(User).filter(User.username == name).filter(User.type == type).one()
        except:
            return None

    """ 
    查询所有记录，按时间排序
    """
    def selectAll(self):
        return db2.session.query(User).order_by(User.created_time)


    """ 
     查询所有记录，按时间排序
    """
    def selectAll(self):
        return db2.session.query(User).order_by(User.created_time)


    """
    分页查询所有
    """
    def selectByPage(self,page_index,type=-1,per_page=10):
        if type == ADMIN:
            pagination = User.query.filter(User.type == 0).order_by(User.created_time).paginate(page_index, per_page)
        elif type == TEACHER:
            pagination = User.query.filter(User.type == 1).order_by(User.created_time).paginate(page_index, per_page)
        else:
            pagination = User.query.order_by(User.created_time).paginate(page_index, per_page)
        return pagination


