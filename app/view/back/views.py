#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

import os
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for

from app.model.config import UPLOAD_FILES_PATH, UPLOAD_PATH
from app.model.entity import Files
from app.service.ArticleService import getArticlesByPage
from app.service.FileServiceV2 import FilesService
from app.service.ProjectServiceV2 import ProjectService
from app.service.UserServiceV2 import UserService, role_dict
from app.view.MessageInfo import MessageInfo
from app.view.back import back

projectService = ProjectService()
filesService = FilesService()
userService = UserService()
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
@back.route("/api/admin/uploadFile",methods=['POST'])
def uploadFile():
    files = request.files.getlist("files")
    if len(files) > 0:
        for f in files:
            file = Files()
            file.name = f.filename  #得到文件名
            file.path = f.filename
            file.source = 0         #代表资料下载的文件
            f.save(os.path.join(UPLOAD_FILES_PATH,file.name))
            filesService.addFile(file)
        return json.dumps(MessageInfo.success(msg="上传成功").__dict__)
    else:
        return json.dumps(MessageInfo.fail(msg="没有检测到文件").__dict__)
@back.route("/admin/editFiles")
def editFiles():
    return render_template('back01/file_add.html')

""" 
管理员删除项目
"""
@back.route("/api/admin/deleteFile")
def deleteFile():
    fid = request.values.get("fid")
    if fid is None:
        return json.dumps(MessageInfo.fail(msg="fid不能为空").__dict__)
    filesService.deleteFileByID(fid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)


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

""" 
下载获奖信息
"""
@back.route("/api/admin/downAwardInfo",methods=['GET'])
def downAwardInfo():
    filename = projectService.generateAwardInfoExcel(None)
    response = make_response(send_from_directory(UPLOAD_PATH, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


""" 
管理员登录接口
"""
@back.route("/api/login",methods=['POST'])
def login_api():
    data = json.loads(request.get_data("utf-8"))
    username = data['username']
    password = data['password']
    user = userService.selectByName(username,0)
    if user :
        if password == user.password:
            session["admin"] = user.username                        #用session保存登录状态
            return json.dumps(MessageInfo.success(msg="登录成功").__dict__)
            # return redirect(url_for("back.main"))
        else:
            return json.dumps(MessageInfo.fail(msg="亲，密码错误!").__dict__)
    else:
        return json.dumps(MessageInfo.fail(msg="亲,用户不存在").__dict__)

@back.route("/api/admin/logout", methods=['GET'])
def logout_api():
    session.pop('admin', None)
    return redirect(url_for('back.login'))
#******************************模板******************************#
""" 
登录页面
"""
@back.route("/login")
def login():
    return render_template("back01/back/login.html")

""" 
后台管理主页
"""
@back.route("/admin/main")
def main():
    return render_template("back01/back/main.html")

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
    return render_template("back01/article_modified.html")

""" 
资料管理
"""
@back.route("/admin/manageResource",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/manageResource/<int:page>/<int:count>",methods=['GET'])
def manageResource(page,count):
    source = request.values.get("source")
    pagination,files = filesService.getFilesBySource(page,count,source)
    print('11111111111')
    for file in files:
        print(file.name)
    return render_template("back01/back/manageResource.html",pagination=pagination,files=files)

""" 
管理员人员管理
"""
@back.route("/admin/manageUser")
def manageUser():
    return render_template("back01/back/manageUser.html")



