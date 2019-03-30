#!/usr/bin/env python
#-*- coding:utf-8 _*-
#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@:author:
@:file: CommonService.py
@:time: 2019/1/3
@:descrition:
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
import base64
import uuid

import os

from flask import session

from app.model.config import UPLOAD_PICS_PATH
class CommonService:


    """
    @:param: arr:base64列表
    @:return:对应的路径列表
    @descrition:将base64编码的图片解码存储本地，并且放回其存储路径。
    """
    def getImgPathList(self,imgdatas):
        if imgdatas is None:
            return None
        ret = []
        for img in imgdatas:
            ret.append(self.base64ToPic(img))
        return ret


    """ 
    @:param:str：base64编码的图片
    @:return:图片名
    @descrition:将base64编码的图片存储到本地
    """
    def base64ToPic(self,data):
        suffix = data[data.find('/') + 1:data.find(';')]                    #得到后缀
        picdata = base64.b64decode(data[data.find(',') + 1:])               #得到base64编码
        picName = str(uuid.uuid1()).replace('-', '') + '.' + suffix
        pic = open(os.path.join(UPLOAD_PICS_PATH, picName), 'wb')
        pic.write(picdata)
        pic.close()
        return picName


    def getCurrentUsername(self,type=-1):
        if type == 0:
            return session['admin']
        elif type == 1:
            return session['student']
        else:
            return "anonymous"
if __name__ == '__main__':
    commonService = CommonService()