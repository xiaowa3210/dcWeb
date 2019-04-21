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
            condition = (Files.delete_flag == 0)
            return self.getFilesByPage(page_index,per_page,condition)
        pagination = Files.query.filter(Files.source == source,Files.delete_flag == 0).paginate(page_index, per_page, error_out=False)
        return pagination,pagination.items


    def getFilesBySourceIdAndSource(self,source,sid):
        files = db2.session.query(Files).filter(Files.source == source, Files.source_id == sid,Files.delete_flag == 0).all()
        db2.session.commit()
        return files

    """ 
    @:param:
        updateContent:更新内容
        condition:查询条件
    @:return:
    @descrition:更新文件
        """
    def updateFileStatus(self, updateContent, condition):
        db2.session.query(Files).filter(condition).update(updateContent)
        db2.session.commit()

    """ 
    @:param:
    @:return:
    @descrition:根据文件ID更新内容
    """
    def updateProStatusByPid(self, updateContent, fid):
        db2.session.query(Files).filter(Files.fid == fid).update(updateContent)
        db2.session.commit()


    """ 
    @:param:
    @:return:
    @descrition:删除文件
    """

    def deletePros(self,source,sid):
        sql = 'update dc_files set delete_flag = 1 where soure = '+ source + ' and source_id =' + 'sid'
        db2.session.execute(sql)
        db2.session.commit()

    def deleteFileByID(self,file_id):
        updateContent = {
            'delete_flag':1
        }
        self.updateProStatusByPid(updateContent,file_id)