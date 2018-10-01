#!/usr/bin/env python 
# _*_ coding: utf-8 _*_

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


from app.view.admin.forms import AddAdminForm, AddProjectForm

import json

from flask import render_template, request

from app.model.models import Laboratory

from app.model.models import *
from app.service.ArticleService import *
from app.utils.timeutils import *
from app.view.MessageInfo import MessageInfo
from app.view.back01 import back01
from datetime import datetime

from flask import Blueprint

api = Blueprint('api', __name__, template_folder='../../../templates')

@api.route('/api/lab', methods=['POST','GET'])
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


