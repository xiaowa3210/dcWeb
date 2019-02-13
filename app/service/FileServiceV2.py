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
from app.model.entity import Files


class FilesService:

    """
    @:param:
    @:return:
    @descrition:添加文件
    """
    def addFile(self,file):
        db2.session.add(file)
        db2.session.commit()

    """ 
    @:param:(page_index)->页数
            (per_page)->每页数量
            (condition)->查询条件
    @:return:
    @descrition:分页查询文件
    """
    def getFilesByPage(self, page_index, per_page,condition):
        if condition is not None:
            pagination = Files.query.filter(condition).paginate(page_index, per_page, error_out=False)
        else:
            pagination = Files.query.paginate(page_index, per_page, error_out=False)
        files = pagination.items
        return pagination, files


    def getFilesBySource(self,page_index, per_page,source):
        if source == '0':#0代表查询全部的
            return self.getFilesByPage(page_index,per_page,None)
        condition = (Files.source == source)
        return self.getFilesByPage(page_index,per_page,condition)

    # 逻辑删除文章,将删除标志位设为1
    def deleteFileByID(self,file_id):
        pass

    def getFileByID(self,file_id):
        pass