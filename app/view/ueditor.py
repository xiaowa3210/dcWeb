#!/usr/bin/env python 
# _*_ coding: utf-8 _*_

'''
ueditor接口
2018.10.01 alex create
插件文档地址“http://fex.baidu.com/ueditor”
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

from app.utils.fileUploadUtils import ftp_upload
from flask import render_template, request

from app.model.models import Laboratory

from app.model.models import *
from app.service.ArticleService import *
from app.utils.timeutils import *
from app.view.MessageInfo import MessageInfo
from app.view.back01 import back01
from datetime import datetime

from flask import Blueprint

ueditor = Blueprint('ueditor', __name__, template_folder='../../../templates')

@ueditor.route('/ueditor/ctrl', methods=['POST','GET'])
def ueditorCtr():
    args = request.args.get("action") or "args没有参数"

    if(args == "config"):#返回编辑器后台配置
        configJSON = open(os.path.abspath('.') + os.sep + 'static' + os.sep + 'config.json', "r", encoding='utf-8').read()
        load_dict = json.loads(configJSON)
        return jsonify(load_dict)


    if(args == "uploadimage"):#接收文件
        print(request)
        if request.method == 'GET':
            return jsonify('{"message":"fail"}')
        else:
            print(request.files)
            print(request.files['upfile'])
            file = request.files['upfile']
            print(file)
            if file:
                localpath = os.path.abspath('.') + os.sep + 'static' + os.sep + 'files' + os.sep + 'images' + os.sep
                print(file.filename)
                mid = datetime.now().strftime('%Y%m%d')
                print(mid)
                filename = file.filename
                file.save(localpath + filename)
                ftp_upload(localpath, filename, 'http://dc.blfly.com/files/images/'+ mid+'/', '/pub/images/' + mid)
        return jsonify('{"message":"success"}')

    if(args == "uploadfile"):#接收文件
        print(request)
        if request.method == 'GET':
            return jsonify('{"message":"fail"}')
        else:
            file = request.files['file']
            print(file)
            if file:
                file.save(file.filename)
        return jsonify('{"message":"success"}')
    else:
        return jsonify('{"message":"fail"}')