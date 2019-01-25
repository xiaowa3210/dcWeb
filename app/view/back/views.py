#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import render_template, request

from app.service.ProjectServiceV2 import ProjectService
from app.view.MessageInfo import MessageInfo
from app.view.back import back

projectService = ProjectService()
#******************************api接口******************************#
""" 
上传新闻
"""
@back.route('/api/uploadNew')
def uploadNew():
    pass

""" 
上传文件
"""
@back.route("/api/uploadFile")
def uploadFile():
    pass

""" 
管理员删除项目
"""
@back.route("/api/admin/deletePro")
def deleteProject():
    pid = request.values.get("pid")
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.deletePro(pid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)

""" 
管理员撤销项目
"""
@back.route("/api/admin/undoPro")
def undoProject():
    pid = request.values.get("pid")
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.undoPro(pid)
    return json.dumps(MessageInfo.success(msg="撤销成功").__dict__)
#******************************模板******************************#
""" 
审核项目
"""
@back.route("/admin/checkproject")
def checkProject():
    return render_template("back01/back/checkproject.html")

""" 
管理项目
"""
@back.route("/admin/manageProject",defaults={'page':1,'count':10})
@back.route("/admin/manageProject/<int:page>/<int:count>")
def manageProject(page,count):
    projects,pagination = projectService.getUploadedProBypage(page,count)
    return render_template("back01/back/manageProject.html",projects=projects,pagination=pagination)



""" 
编辑新闻
"""
@back.route("/admin/editNews")
def editNews():
    return render_template("back01/back/editNews.html")

""" 
新闻管理
"""
@back.route("/admin/manageNews")
def manageNews():
    return render_template("back01/back/manageNews.html")

""" 
修改新闻
"""
@back.route("/admin/modifiesNews")
def modifiesNews():
    return render_template("back01/back/modifiesNews.html")

""" 
资料管理
"""
@back.route("/admin/manageResource")
def manageResource():
    return render_template("back01/back/manageResource.html")


""" 
管理员人员管理
"""
@back.route("/admin/manageUser")
def manageUser():
    return render_template("back01/back/manageUser.html")



