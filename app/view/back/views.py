#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

import os
import uuid

from datetime import datetime
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for

from app.model.config import UPLOAD_FILES_PATH, UPLOAD_PATH, UEDITOR_UPLOAD_PATH, UPLOAD_AWARD_PATH
from app.model.entity import Files, User, New, newExt
from app.service.NewsService import NewsService
from app.service.FileServiceV2 import FilesService
from app.service.ProjectServiceV2 import ProjectService
from app.service.UserServiceV2 import UserService, role_dict
from app.view.MessageInfo import MessageInfo
from app.view.back import back
from app.service.CommonService import CommonService

commonService = CommonService()
projectService = ProjectService()
filesService = FilesService()
userService = UserService()
newsService = NewsService()
#******************************api接口******************************#
"""
添加新闻
"""
@back.route('/api/admin/addNew',methods=['POST'])
def uploadNew():
    title = request.form.get("title")
    content = request.form.get("content")
    src_content = request.form.get("src_content")
    type = request.form.get('type')
    operate = request.form.get('operate')
    attachments = request.files.getlist("attachment")
    # isTop = request.form.get('radio')

    # if isTop=='1':
    #     print("置顶")
    # else:
    #     print("不置顶")
    #todo:需处理是否置顶
    if operate == '0':
        #代表添加新闻
        new = New(title, content, src_content)

        extraInfo = newExt(title, type)
        extraInfo.creater = commonService.getCurrentUsername(0)
        extraInfo.modifiedTime = datetime.now()
        extraInfo.modifier = commonService.getCurrentUsername(0)
        extraInfo.status = type
        if type == '1':#代表发布新闻
            extraInfo.publisher = commonService.getCurrentUsername(0)
            extraInfo.publisherTime = datetime.now()
        new.extInfo = extraInfo
        newsService.addNews(new)


        ###添加附件
        files = []
        if len(attachments) > 0:
            path = UEDITOR_UPLOAD_PATH + "/files/"
            if not os.path.exists(path):
                os.mkdir(path)
            for attachment in attachments:
                file = Files()
                file.name = attachment.filename
                suffix = file.name[file.name.rfind('.'):]
                local_path = str(uuid.uuid1()).replace("-", "") + suffix
                attachment.save(path + local_path)
                file.path = local_path
                file.source = 4                                 #代表新闻附件
                file.source_id = new.nid
                filesService.addFile(file)

        return json.dumps(MessageInfo.success(msg="添加成功").__dict__)
    else:
        nid = request.form.get("nid")
        new = New(title, content, src_content)
        new.nid = nid
        newsService.updatenew(new,type)



        ###添加附件
        files = []
        if len(attachments) > 0:
            path = UEDITOR_UPLOAD_PATH + "/files/"
            if not os.path.exists(path):
                os.mkdir(path)
            for attachment in attachments:
                file = Files()
                file.name = attachment.filename
                suffix = file.name[file.name.rfind('.'):]
                local_path = str(uuid.uuid1()).replace("-", "") + suffix
                attachment.save(path + local_path)
                file.path = local_path
                file.source = 4  # 代表新闻附件
                file.source_id = new.nid
                filesService.addFile(file)
        return json.dumps(MessageInfo.success(msg="修改成功").__dict__)

"""
删除新闻
"""
@back.route('/api/admin/deleteNew/<nid>',methods=['get'])
def deteteNew(nid):
    newsService.deleteNew(nid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)

"""
发布新闻
"""
@back.route('/api/admin/releaseNew/<nid>',methods=['get'])
def releaseNew(nid):
    newsService.releaseOrUndoNew(nid,1)
    return json.dumps(MessageInfo.success(msg="发布成功").__dict__)

"""
撤销新闻
"""
@back.route('/api/admin/undoNew/<nid>',methods=['get'])
def undoNew(nid):
    newsService.releaseOrUndoNew(nid,0)
    return json.dumps(MessageInfo.success(msg="撤销成功").__dict__)

"""
审核新闻
"""
@back.route('/api/admin/checkNew/<int:nid>/<int:op>',methods=['get'])
def checkNew(nid,op):
    status = 3 if op == 1 else 1
    newsService.updateNewStatusByNid({
        'status': status
    },nid)
    return json.dumps(MessageInfo.success(msg="审核完成").__dict__)

"""
上传文件
"""
@back.route("/api/admin/uploadFile",methods=['POST'])
def uploadFile():
    files = request.files.getlist("attachment")
    if len(files) > 0:
        for f in files:
            file = Files()
            file.name = f.filename  #得到文件名
            suffix = file.name[file.name.rfind('.'):]
            local_path = str(uuid.uuid1()).replace("-", "") + suffix
            file.path = local_path
            file.source = 2             #代表资料下载的文件
            file.source_id = -1         #资料没有与之关联的source_id。所以设为1
            f.save(os.path.join(UPLOAD_FILES_PATH,local_path))
            filesService.addFile(file)
        return json.dumps(MessageInfo.success(msg="上传成功").__dict__)
    else:
        return json.dumps(MessageInfo.fail(msg="没有检测到文件").__dict__)
"""
管理员删除资源
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
@back.route("/api/admin/deletePro",methods=['POST'])
def deleteProject():
    pid = request.values.get('pid')
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.deletePro(pid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)

"""
管理员撤销项目
"""
@back.route("/api/admin/undoPro", methods=['POST'])
def undoProject():
    pid = request.values.get('pid')
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
    data = json.loads(request.get_data(as_text=True))
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
生成获奖信息
"""
@back.route("/api/admin/exportAwardInfo",methods=['GET'])
def exportAwardInfo():
    #筛选条件
    startTime = request.args.get('startTime', default=None)
    endTime = request.args.get('endTime', default=None)
    rank = request.args.get('rank', default=-1)
    pagination, awards = projectService.selectAwardInfo(startTime, endTime, rank, 1, 10000)

    #根据获奖信息导出文件名
    filename = projectService.exportAwardInfo(awards)
    response = make_response(send_from_directory(UPLOAD_AWARD_PATH, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

"""
下载获奖信息
"""
@back.route("/api/admin/downAwardInfo",methods=['GET'])
def downAwardInfo():
    filename = projectService.generateAwardInfoExcel(None)
    response = make_response(send_from_directory(UPLOAD_AWARD_PATH, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


"""
管理员登录接口
"""
@back.route("/api/login",methods=['POST'])
def login_api():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    password = data['password']
    type = data['type']
    user = userService.selectByName(username,type)
    if user:
        if password == user.password:
            info = {'name':user.username,'type':user.type}
            session["admin"] = info                                     #用session保存登录状态
            return json.dumps(MessageInfo.success(msg="登录成功").__dict__)
            # return redirect(url_for("back.main"))
        else:
            return json.dumps(MessageInfo.fail(msg="亲，密码错误!").__dict__)
    else:
        return json.dumps(MessageInfo.fail(msg="亲,用户不存在").__dict__)

"""
管理员登出接口
"""
@back.route("/api/admin/logout", methods=['GET'])
def logout_api():
    session.pop('admin', None)
    return redirect(url_for('front.home'))

"""
管理员添加用户
"""
@back.route("/api/admin/addUser", methods=['POST'])
def addUser():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    password = data['password']
    type = data['type']

    user = User(username,password,type)
    userService.addUser_v1(user)
    return json.dumps(MessageInfo.success(msg="添加成功").__dict__)


"""
管理员删除用户
"""
@back.route("/api/admin/deleteUser", methods=['POST'])
def deleteUser():
    data = json.loads(request.get_data(as_text=True))
    uid = data['uid']

    userService.deleteUser(uid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)

#******************************模板******************************#
#******************************模板******************************#
#******************************模板******************************#
#******************************模板******************************#
#******************************模板******************************#
#******************************模板******************************#

"""
登录页面
"""
@back.route("/login")
def login():
    return render_template("back/login.html")

"""
后台管理主页
"""
@back.route("/admin/main")
def main():
    return render_template("back/main.html")


@back.route("/admin/addUser")
def insertUser():
    return render_template("back/addUser.html")

"""
审核项目
"""
@back.route("/admin/checkproject/<int:pid>")
def checkProject(pid):
    project = projectService.getProjectByID(pid)
    #若是未提交状态管理员就没必要查看其内容
    # if project.status == 1 or project.delete_flag == 1:
    #     project = None
    return render_template("back/checkproject.html",project=project)

"""
审核项目列表
"""
@back.route("/admin/checkProjects",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/checkProjects/<int:page>/<int:count>")
def checkProjects(page,count):
    pagination,projects = projectService.getUncheckPro(page,count)
    return render_template("back/checkProjects.html",projects=projects,pagination=pagination)

"""
管理项目
"""
@back.route("/admin/manageProject",defaults={'page':1,'count':10})
@back.route("/admin/manageProject/<int:page>/<int:count>")
def manageProject(page,count):
    pagination,projects = projectService.getUploadedProBypage(page,count)
    return render_template("back/manageProject.html",projects=projects,pagination=pagination)


@back.route("/admin/deleteProject",defaults={'page':1,'count':10})
@back.route("/admin/deleteProject/<int:page>/<int:count>")
def editeProject(page,count):
    # 筛选条件
    startTime = request.args.get('startTime', default=None)
    endTime = request.args.get('endTime', default=None)
    type = request.args.get('type', default=-1)
    major = request.args.get('major', default=0)
    pagination, projects = projectService.getPublishedPro(page, count,startTime=startTime,
                                                         endTime=endTime,
                                                         type=type,
                                                         major=major)
    return render_template("back/deleteProject.html",projects=projects,pagination=pagination)


"""
编辑新闻
"""
@back.route("/admin/editNews")
def editNews():
    return render_template('back/article_add.html')

"""
新闻管理
"""
#文章列表
@back.route('/admin/manageNews', methods=['GET'],defaults={'page':1,'count':10})
@back.route('/admin/manageNews/<int:page>/<int:count>',methods=['GET'])
def manageNews(page,count):
    type = request.values.get("type")
    pagination, news = newsService.selectByPage(page, count, type)

    # 已经发布是status=0， 未发布status=1
    if(type == '-1'):
        return render_template('back/article_list.html', news=news, pagination=pagination)
    elif (type == '0'):
        return render_template('back/article_list_unpublished.html', news=news, pagination=pagination)
    elif(type == '1'):
        return render_template('back/article_list_published.html', news=news, pagination=pagination)





"""
修改新闻
"""
@back.route("/admin/modifiesNews/<int:nid>")
def modifiesNews(nid):
    new = newsService.selectByNid(nid)
    files = filesService.getFilesBySourceIdAndSource(4,nid)
    return render_template("back/modifiesNews.html",article=new,files=files)

"""
资料管理
"""
@back.route("/admin/manageResource",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/manageResource/<int:page>/<int:count>",methods=['GET'])
def manageResource(page,count):
    source = request.values.get("source")
    pagination,files = filesService.getFilesBySource(page,count,source)
    if(source == '0'):
        return render_template("back/manageResource_all.html",pagination=pagination,files=files)
    elif (source == '1'):
        return render_template("back/manageResource_admin.html",pagination=pagination,files=files)
    elif (source == '2'):
        return render_template("back/manageResource_article.html", pagination=pagination, files=files)
    else:
        return render_template("back/manageResource_project.html", pagination=pagination, files=files)

@back.route("/admin/editFiles")
def editFiles():
    return render_template('back/file_add.html')
"""
管理员人员管理
"""
@back.route("/admin/manageUser",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/manageUser/<int:page>/<int:count>",methods=['GET'])
def manageUser(page,count):
    type = request.values.get("type")
    pagination, users = userService.selectByPage(page,count,type)
    return render_template("back/manageUser.html",pagination=pagination,users=users)


"""
审核新闻列表
"""
@back.route("/admin/checkNewsView",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/checkNewView/<int:page>/<int:count>",methods=['GET'])
def checkNewView(page,count):
    pagination, news = newsService.selectByPage(page, count, 2)
    return render_template("back/checkArticles.html",pagination=pagination,news=news)

"""
审核新闻
"""
@back.route("/admin/newPreview",methods=['GET'])
@back.route("/admin/newPreview/<int:nid>")
def newPreview(nid):
    new = newsService.selectByNid(nid)
    return render_template("back/checknew.html",new = new)

"""
管理员(非超级管理员)管理自己新闻
"""
@back.route('/adminNews', methods=['GET'],defaults={'page':1,'count':10})
@back.route('/admin/adminNews/<int:page>/<int:count>',methods=['GET'])
def adminNews(page,count):
    status = request.values.get("status")
    username = session['admin']['name']
    pagination, news = newsService.selectByUsername(page, count, status,username)
    return render_template('back/article_list.html', news=news, pagination=pagination,status = status)

'''
获取项目获奖信息
'''
@back.route("/admin/getAwards",methods=['GET'],defaults={'page':1,'count':10})
@back.route("/admin/getAwards/<int:page>/<int:count>")
def getAwards(page, count):
    #筛选条件
    startTime = request.args.get('startTime', default=None)
    endTime = request.args.get('endTime', default=None)
    rank = request.args.get('rank', default=-1)
    pagination, awards = projectService.selectAwardInfo(startTime, endTime, rank, page, count)
    return render_template("back/awards_list.html", pagination=pagination, awards=awards)