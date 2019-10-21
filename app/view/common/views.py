#!/user/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:
@file: views.py
@time: 2019/1/2
@descrition:前台后台公共的api接口

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
import json
import os
import uuid

from datetime import datetime
from flask import request, url_for, jsonify, Response, make_response, send_from_directory

from app import MessageInfo
from app.model.config import UPLOAD_PICS_PATH, UPLOAD_FILES_PATH, UEDITOR_UPLOAD_PATH
from app.model.entity import Files
from app.service.FileServiceV2 import FilesService
from app.view.common import common


filesService = FilesService()
""" 
markdown上传图片接口
"""
@common.route('/markdown/upload/',methods=['POST'])
def markdown_upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': u'图片格式异常'
        }
    else:
        ex = os.path.splitext(file.filename)[1]  # 文件的后缀
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(UPLOAD_PICS_PATH, filename))
        # 返回
        res = {
            'success': 1,
            'message': u'图片上传成功',
            'url': url_for('common.image', name=filename)
        }
    return jsonify(res)

""" 
根据文件名，下载图片接口
"""
@common.route('/image/<name>')
def image(name):
    with open(os.path.join(UPLOAD_PICS_PATH,name),'rb') as f:
        resp=Response(f.read(),mimetype="image/jpeg")
    return resp


""" 
上传图片，
source代表来源。#1.代表封面图片，3:获奖证书图片。
source_id代表来源(来源暂时有封面图片,获奖证书)，若没有就设为-1。
"""
@common.route('/api/addPic',methods=['POST'])
def addPic():
    files = request.files.getlist("pics")
    source = request.form.get("source")
    source_id = request.form.get("source_id")
    source_id = source_id if source_id else -1
    if len(files) > 0:
        path = UEDITOR_UPLOAD_PATH + "/pics/"
        if not os.path.exists(path):
            os.mkdir(path)
        ret = []
        for f in files:
            file = Files()
            file.name = f.filename
            suffix = file.name[file.name.rfind('.'):]
            local_path = str(uuid.uuid1()).replace("-", "") + suffix
            file.path = local_path
            file.source = source
            file.source_id = source_id
            f.save(path + local_path)  # 保存文件到本地
            filesService.addFile(file)  # 将文件信息写入到数据库
            info = {
                'url': url_for('common.image', name=local_path),
                'id':file.fid
            }
            ret.append(info)

        return json.dumps(MessageInfo.success(msg='保存成功', data=ret).__dict__)

""" 
根据文件名，下载文件
"""
@common.route('/file/<name>')
def file(name):
    response = make_response(send_from_directory(UPLOAD_FILES_PATH, name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(name.encode().decode('latin-1'))
    return response


""" 
根据文件名，下载文件
"""
@common.route('/zip/<name>')
def zip(name):
    response = make_response(send_from_directory(UPLOAD_ZIP_PATH, name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(name.encode().decode('latin-1'))
    return response

""" 
根据文件名，下载文件
"""
@common.route('/hello')
def hello():
    return "hello"





