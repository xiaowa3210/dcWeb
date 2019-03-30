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
import os

from datetime import datetime
from flask import request, url_for, jsonify, Response, make_response, send_from_directory
from dcwebapp.model.config import UPLOAD_PICS_PATH, UPLOAD_FILES_PATH
from dcwebapp.view.common import common



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
根据文件名，下载文件
"""
@common.route('/file/<name>')
def file(name):
    response = make_response(send_from_directory(UPLOAD_FILES_PATH, name, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(name.encode().decode('latin-1'))
    return response




