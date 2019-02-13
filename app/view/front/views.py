#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import request, render_template

from app.service.FileServiceV2 import FilesService
from app.service.ProjectServiceV2 import ProjectService
from app.view.MessageInfo import MessageInfo
from app.view.front import front

projectService = ProjectService()
filesService = FilesService()
#******************************api接口******************************#
""" 
上传项目接口
"""
@front.route('/api/uploadProject',methods=['POST'])
def uploadProject():
    #数据
    data = json.loads(request.get_data("utf-8"))
    projectService.addProject(data)
    return json.dumps(MessageInfo.success(data='保存成功').__dict__)

""" 
上传图片接口
"""
@front.route('/api/uploadImg')
def uploadImg():
    pass

""" 
学生撤销审核中的项目
"""
@front.route('/api/student/undoPro')
def stuUodoPro():
    pid = request.values.get("pid")
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.stuUndoPro(pid)
    return json.dumps(MessageInfo.success(msg="撤销成功").__dict__)
#******************************模板******************************#

""" 
管理项目
"""
@front.route('/student/manageProject',defaults={'page':1,'count':10})
@front.route('/student/manageProject/<int:page>/<int:count>')
def manageProject(page,count):
    pagination,project = projectService.getProByStudentId(page,count)
    return render_template("tmp01/manageProject.html",pagination=pagination,project=project)

""" 
修改项目
"""
@front.route('/student/modifiesProject/<int:pid>')
def modifiesProject(pid):
    project = projectService.getProjectByID(pid)
    return render_template("tmp01/modifiesProject.html",project=project)

""" 
上传项目
"""
@front.route('/student/uploadProject')
def uploadProjectTmp():
    return render_template("tmp01/addProject.html")

""" 
新闻列表展示
"""
@front.route('/news')
def news():
    return render_template("tmp01/news.html")

""" 
新闻内容展示
"""
@front.route('/new')
def new():
    return render_template("tmp01/new.html")

"""
资料下载展示
"""
@front.route('/downloadfile',defaults={'page':1,'count':10})
@front.route('/downloadfile/<int:page>/<int:count>')
def downloadFile(page,count):
    pagination, files = filesService.getFilesBySource(page, count, '0')
    return render_template("tmp01/downlink.html", pagination=pagination, files=files)

""" 
基地风采展示
"""
@front.route("/lab")
def lab():
    return render_template("tmp01/lab.html")


