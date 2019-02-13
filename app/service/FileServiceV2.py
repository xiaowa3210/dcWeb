#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@:author:
@:file: FileServiceV2.py
@:time: 2019/2/13
@:descrition:文件操作业务逻辑类

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
from app import db2


class FilesService:

    """
    @:param:
    @:return:
    @descrition:添加文件
    """
    def addFile(self,file):
        db2.session.add(file)
        db2.session.commit()

    # 逻辑删除文章,将删除标志位设为1
    def deleteFileByID(self,file_id):
        pass

    def getFileByID(self,file_id):
        pass

    def getFilesByPage(self,page_index, per_page):
        pass