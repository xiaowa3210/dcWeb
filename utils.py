# -*- coding: utf-8 -*-

import html
import json
import datetime
from urllib.parse import unquote
# from admin.backstage.models import CfgNotify
from flask import Response, flash
from app.models import Document, Project, User, Role, Permission
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

def getDoucumentByID(did):
    return db.session.query(Document).filter(Document.id == did).one()


def getDocumentByPage(page_index, per_page,type):
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page_index, per_page)
    documents = pagination.items
    return pagination,documents

def getProjectsByPage(page_index,per_page):
    # 这个地方要用到分页查询，每次查询12页
    pagination = Project.query.paginate(page_index, per_page, error_out=False)
    projects = pagination.items
    return pagination,projects

def getProjectById(pid):
    return Project.query.filter(Project.id == pid).one()


## 字符串转字典
def str_to_dict(dict_str):
    if isinstance(dict_str, str) and dict_str != '':
        new_dict = json.loads(dict_str)
    else:
        new_dict = ""
    return new_dict


## URL解码
def urldecode(raw_str):
    return unquote(raw_str)


# HTML解码
def html_unescape(raw_str):
    return html.unescape(raw_str)


## 键值对字符串转JSON字符串
def kvstr_to_jsonstr(kvstr):
    kvstr = urldecode(kvstr)
    kvstr_list = kvstr.split('&')
    json_dict = {}
    for kvstr in kvstr_list:
        key = kvstr.split('=')[0]
        value = kvstr.split('=')[1]
        json_dict[key] = value
    json_str = json.dumps(json_dict, ensure_ascii=False, default=datetime_handler)
    return json_str


# 字典转对象
def dict_to_obj(dict, obj, exclude=None):
    for key in dict:
        if exclude:
            if key in exclude:
                continue
        setattr(obj, key, dict[key])
    return obj


# peewee转dict
def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['_data']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict


# peewee转list
def query_to_list(query, exclude=None):
    list = []
    for obj in query:
        dict = obj_to_dict(obj, exclude)
        list.append(dict)
    return list


# 封装HTTP响应
def jsonresp(jsonobj=None, status=200, errinfo=None):
    if status >= 200 and status < 300:
        jsonstr = json.dumps(jsonobj, ensure_ascii=False, default=datetime_handler)
        return Response(jsonstr, mimetype='application/json', status=status)
    else:
        return Response('{"errinfo":"%s"}' % (errinfo,), mimetype='application/json', status=status)


# 通过名称获取PEEWEE模型
# def get_model_by_name(model_name):
#     if model_name == 'notifies':
#         DynamicModel = CfgNotify
#     else:
#         DynamicModel = None
#     return DynamicModel


# JSON中时间格式处理
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Unknown type")


# wtf表单转peewee模型
def form_to_model(form, model):
    for wtf in form:
        model.__setattr__(wtf.name, wtf.data)
    return model


# peewee模型转表单
def model_to_form(model, form):
    dict = obj_to_dict(model)
    form_key_list = [k for k in form.__dict__]
    for k, v in dict.items():
        if k in form_key_list and v:
            field = form.__getitem__(k)
            field.data = v
            form.__setattr__(k, field)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("字段 [%s] 格式有误,错误原因: %s" % (
                getattr(form, field).label.text,
                error
            ))
