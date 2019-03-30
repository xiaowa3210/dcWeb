#!/usr/bin/env python 
# _*_ coding: utf-8 _*_
from dcwebapp.service.DocumentsService import getDocumentByPage
'''
api是用于获取信息的接口
2018.10.01 alex create
'''

import datetime
import time

import os
from os import path

from flask import render_template, flash, request, url_for, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename, redirect


from dcwebapp.view.admin.forms import AddAdminForm, AddProjectForm

import json

from flask import render_template, request

from dcwebapp.model.models import Laboratory

from dcwebapp.model.models import *
from dcwebapp.service.ArticleService import *
from dcwebapp.utils.timeutils import *
from dcwebapp.view.MessageInfo import MessageInfo
from dcwebapp.view.back01 import back01
from datetime import datetime

from flask import Blueprint
from dcwebapp.utils.utils import object2json
api = Blueprint('api', __name__, template_folder='../../../templates')

'''获取新闻文档的接口，传递参数:article id'''
@api.route('/getArticleById', methods=['POST', 'GET'])
def articleByKey():
    if(request.json == None):        json_data = request.form
    else:        json_data = json.loads(json.dumps(request.json))#解析前端传过来的json数据
    articleId = str(json_data['articleId'])
    article = getArticleByID(articleId)
    if(article == [] or article == None):
        return {'message': 'fail'}#为空返回fail
    '''python居然没有一个对象转json的可用方法！！！还得自己现编一个！！！'''
    objson = object2json(article)
    print(objson)
    return jsonify({'message':'success','data': objson})
'''
查询实验室？
此条不是alex写的
'''
@api.route('/lab', methods=['POST','GET'])
def lab():
    print(request.json)

    #解析前端传过来的json数据

    s1 = json.dumps(request.json)
    data = json.loads(s1)
    keyword = data['keyword']
    lab = Laboratory.query.filter_by(name=keyword).first()
    if(lab == None):
        return jsonify({'id':"none", 'title':"none"});
    id=lab.id
    title = lab.name

    return jsonify({'id':id, 'title':title})

'''
此条已废弃
获取新闻文档的接口
传递参数:时间，条数，页数
全部为int类型
'''
@api.route('/doc', methods=['POST','GET'])
def doc():
    print(request.json)
    if(request.json == None):
        json_data = request.form
        print(json_data)
    else:
        json_data = json.loads(json.dumps(request.json))#解析前端传过来的json数据
    per_page = int(json_data['rows'])
    page = int(json_data['pageNum'])
    doctype = int(json_data['type'])
    pagination, documents = getDocumentByPage(page, per_page, doctype)
    if(documents == [] or documents == None):
        return {'message': 'fail'}#为空返回fail
    print(documents), print(documents[0].content)
    docs = {}
    i = 0
    for doc in documents:
        #if(i):break
        docs[i] = {}; docs[i]['title'] = doc.title; docs[i]['content'] = doc.content
        i += 1

    return json.dumps({'message':'success','data': docs})


