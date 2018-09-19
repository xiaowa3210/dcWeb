#!usr/bin/python
# -*- coding: utf-8 -*-
from ..models import User, Role, Permission
from app import db

#添加用户,添加用户的时候需要注明用户的类型。
def addUser(username,password,roleId):
    user = User(username,password)
    db.session.add(user)
    user = db.session.query(User).filter(User.username == username).one()
    print(user.id)
    if user.id:
        sql = 'INSERT INTO t_user_role VALUES ( '+ str(user.id) + ',' + str(roleId)+ ')'
        print(sql)
        db.session.execute(sql)
    else:
        db.session.rollback()
    db.session.commit()
    return user

#根据ID删除用户,注意先后顺序。先删除外键数据。
def deleteUserByUserId(userID):
    try:
        # 删除t_user_role中关联的数据
        sql = 'delete from t_user_role where userId=' + str(userID)
        db.session.execute(sql)
        # 删除t_user_project中关联的数据
        sql = 'delete from t_user_project where userId=' + str(userID)
        # 删除t_user中的数据
        sql = 'delete from t_user where id=' + str(userID)
        db.session.execute(sql)
        db.session.execute(sql)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True

#根据用户名删除用户
def deleteUserByUsername(username):
    user = getUserByUsername(username)
    return deleteUserByUserId(user.id)

#修改密码
def modifyPasswordByUserId(userId, newpwd):
    try:
        db.session.query(User).filter(User.id == userId).update({User.password:newpwd})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

#根据id查询用户信息
def getUserById(userID):
    return db.session.query(User).filter(User.id == userID).one()


#根据用户名查询用户信息
def getUserByUsername(username):
    return db.session.query(User).filter(User.username == username).one()

#添加角色
def addRole(rolename):
    role = Role(rolename)
    db.session.add(role)
    db.session.commit()

#添加权限
def addPermission(name,label):
    permission = Permission(name,label)
    try:
        db.session.add(permission)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True