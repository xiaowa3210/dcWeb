#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import render_template, request

from app.service.ArticleService import getArticlesByPage
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


""" 
审核项目接口
分为2种。operation：0代表不通过审核，1代表通过审核
通过或者不通过审核可以给出相应的msg
"""
@back.route("/api/admin/checkoutPro",methods=['POST'])
def checkoutProjectapi():
    data = json.loads(request.get_data("utf-8"))
    pid = data["pid"]
    project = projectService.getProStatusByPid(pid)
    if project.delete_flag == 1:
        return json.dumps(MessageInfo.fail(msg="亲,该项目已删除不能对它进行操作了").__dict__)
    if project.status == 1:
        return json.dumps(MessageInfo.fail(msg="亲,该项目还未提交，暂时不能对其操作").__dict__)
    operation = data["operation"]
    msg = data["msg"]
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.checkoutPro(pid,operation,msg)
    return json.dumps(MessageInfo.success(msg="审核成功").__dict__)
#******************************模板******************************#
""" 
审核项目
"""
@back.route("/admin/checkproject/<int:pid>")
def checkProject(pid):
    project = projectService.getProStatusByPid(pid)
    #若是未提交状态管理员就没必要查看其内容
    if project.status == 1 or project.delete_flag == 1:
        project = None
    return render_template("back01/back/checkproject.html",project=project)

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
    return render_template('back01/article_add.html')

""" 
新闻管理
"""
#文章列表
@back.route('/admin/manageNews', methods=['GET'],defaults={'page':1})
@back.route('/admin/manageNews/<int:page>',methods=['GET'])
def manageNews(page):
    articles, pagination = getArticlesByPage(page, 10, 1)
    return render_template('back01/article_list.html', articles=articles, pagination=pagination)

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



