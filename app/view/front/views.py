#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import request, render_template

from app.service.ProjectServiceV2 import ProjectService
from app.view.MessageInfo import MessageInfo
from app.view.front import front

projectService = ProjectService()

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


#******************************模板******************************#

""" 
管理项目
"""
@front.route('/student/manageProject')
def manageProject():
    return render_template("tmp01/manageProject.html")

""" 
修改项目
"""
@front.route('/student/modifiesProject')
def modifiesProject():
    return render_template("tmp01/modifiesProject.html")

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
@front.route('/downloadfile')
def downloadFile():
    return render_template("tmp01/downloadfile.html")

""" 
基地风采展示
"""
@front.route("/lab")
def lab():
    return render_template("tmp01/lab.html")


