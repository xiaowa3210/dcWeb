#!usr/bin/python
# -*- coding: utf-8 -*-

import html
import json
import datetime
from urllib.parse import unquote
from flask import Response, flash
import time

## 字符串转字典
def str_to_dict(dict_str):
    if isinstance(dict_str, str) and dict_str != '':
        new_dict = json.loads(dict_str)
    else:
        new_dict = ""
    return new_dict

def str_to_list(list_str):
    if isinstance(list_str, str) and list_str != '':
        new_list = json.loads(list_str)
    else:
        new_list = ""
    return new_list


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

#对象转json
def object2json(obj):
    objson = {}
    for k,v in obj.__dict__.items(): objson[k] = str(v)
    return objson


def mapGet(map,key):
    if key in map.keys():
        return map[key]
    else:
        return None



def member2dict(member):
    return {
        'id': member.id,
        'pid':member.pid,
        'name': member.name,
        'academy': member.academy,
        'grade': member.grade,
        'type': member.type,
        'major': member.major,
        'number': member.number,
        'classId': member.classId,
    }



def award2dict(award):
    return {
        'id': award.id,
        'awardName':award.awardName,
        'awardTime': award.awardTime,
        'rank': award.rank,
        'pics':award.pics
    }