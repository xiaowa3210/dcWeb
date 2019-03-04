#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import request, render_template, session

from app.service.UserServiceV2 import UserService
from app.service.FileServiceV2 import FilesService
from app.service.NewsService import NewsService
from app.service.ProjectServiceV2 import ProjectService
from app.view.MessageInfo import MessageInfo
from app.view.front import front

projectService = ProjectService()
filesService = FilesService()
newsService = NewsService()
userService = UserService()
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
学生登录接口
"""
@front.route("/student/api/login",methods=['POST'])
def stu_login_api():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    password = data['password']
    user = userService.selectByName(username,1)
    if user :
        if password == user.password:
            session["student"] = user.username                                    #用session保存登录状态
            return json.dumps(MessageInfo.success(msg="登录成功").__dict__)
            # return redirect(url_for("back.main"))
        else:
            return json.dumps(MessageInfo.fail(msg="亲，密码错误!").__dict__)
    else:
        return json.dumps(MessageInfo.fail(msg="亲,用户不存在").__dict__)

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

""" 
学生删除的项目
"""
@front.route('/api/student/deletePro',methods=['POST'])
def studeletePro():
    data = json.loads(request.get_data("utf-8"))
    pid = data["pid"]
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.deletePro(pid)
    return json.dumps(MessageInfo.success(msg="删除成功").__dict__)
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
@front.route('/news', methods=['GET'],defaults={'page':1,'count':10})
@front.route('/news/<int:page>/<int:count>')
def news(page,count):
    pagination, news = newsService.selectByPage(page, count, 1)
    return render_template("tmp01/news.html",pagination=pagination,documents=news)

""" 
新闻内容展示
"""
@front.route('/new/<news_id>')
def new(news_id):
    new = newsService.selectByNid(news_id)
    return render_template("tmp01/news-detail.html",new=new)

"""
资料下载展示
"""
@front.route('/downloadfile',defaults={'page':1,'count':10})
@front.route('/downloadfile/<int:page>/<int:count>')
def downloadFile(page,count):
    pagination, files = filesService.getFilesBySource(page, count, '0')
    return render_template("tmp01/downlink.html", pagination=pagination, files=files)

""" 
项目分页展示
"""
@front.route("/projects",methods=['GET'],defaults={'page':1,'count':10})
@front.route("/projects/<int:page>/<int:count>")
def projects(page,count):
    pagination,projects = projectService.getPublishedPro(page,count)
    return render_template("tmp01/projects.html",projects=projects,pagination=pagination)

""" 
项目详细展示
"""
@front.route("/project",methods=['GET'])
@front.route("/project/<int:pid>")
def project(pid):
    project = projectService.getProjectByID(pid)
    return render_template("tmp01/projects.html",project=project)

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
@front.route("/home")
def home():
   pagination,projects = projectService.getPublishedPro(1,4)
   return render_template("tmp01/home.html",projects=projects,pagination=pagination)

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

@front.route("/student/login")
def stu_login():
    return render_template("tmp01/login.html")