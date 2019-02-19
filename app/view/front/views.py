#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import request, render_template

from app.service.FileServiceV2 import FilesService
from app.service.DocumentsService import getDoucumentByID, getAiticleByID
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
@front.route('/api/student/undoPro',methods=['POST'])
def stuUodoPro():
    data = json.loads(request.get_data("utf-8"))
    pid = data["pid"]
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
    return render_template("tmp01/user.html",pagination=pagination,project=project)

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
@front.route('/new/<news_id>')
def new(news_id):
    news_obj = getAiticleByID(news_id)
    return render_template("tmp01/news-detail.html",news=news_obj)

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

@front.route("/lab/i3")
def i3():
    return render_template('tmp01/i3.html')

"""
主页
"""
#@front.route("/home")
#def home():
#    return render_template("tmp01.home")  #按项目发布时间排序，取最近的4个项目，需要：项目名称、封面图片、发布人和时间

"""
用户中心
"""
#@front.route("/user/<user_id>")
#def user(user_id):
#    return render_template("tmp01/user.html") #根据学生的id获取到学生Model

"""
测试用
"""
@front.route("/user")
def user():
    return render_template("tmp01/user.html")