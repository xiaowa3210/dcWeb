#!/user/bin/env python
# -*- coding:utf-8 -*-
import base64
import json
from flask import request, render_template, session, redirect, url_for
from app.model.entity import User
from app.service.UserServiceV2 import UserService
from app.service.FileServiceV2 import FilesService
from app.service.NewsService import NewsService
from app.service.ProjectServiceV2 import ProjectService
from app.utils.email import send_mail
from app.utils.utils import object2json, member2dict, award2dict
from app.view.MessageInfo import MessageInfo
from app.view.front import front

projectService = ProjectService()
filesService = FilesService()
newsService = NewsService()
userService = UserService()
#******************************api接口******************************#


#######################项目上传相关api##################################

"""
添加项目接口
"""
@front.route('/api/addPro',methods=['POST'])
def addProject():
    data = json.loads(request.get_data(as_text=True))
    pid = projectService.addPro(data)
    return json.dumps(MessageInfo.success(msg='保存成功',data={
        'pid':pid
    }).__dict__)

"""
添加项目成员
"""
@front.route('/api/addProMember/<int:type>/<int:pid>',methods=['POST'])
def addProMember(type,pid):
    data = json.loads(request.get_data(as_text=True))
    mid = projectService.addProMember(pid,data,type)
    return json.dumps(MessageInfo.success(msg='添加成功',data={
        'mid':mid
    }).__dict__)


"""
添加获奖信息
"""
@front.route('/api/addProAward/<int:pid>',methods=['POST'])
def addProAward(pid):
    data = json.loads(request.get_data(as_text=True))
    mid = projectService.addAwardInfo(pid,data)
    return json.dumps(MessageInfo.success(msg='添加成功',data={
        'id':mid
    }).__dict__)


"""
得到成员信息
"""
@front.route('/api/member/<int:mid>',methods=['GET'])
def getMember(mid):
    member = projectService.getMember(mid)
    memberJson = json.dumps(member,default=member2dict)
    return json.dumps(MessageInfo.success(msg='保存成功',data=memberJson).__dict__)


"""
得到获奖信息
"""
@front.route('/api/award/<int:aid>',methods=['GET'])
def getAward(aid):
    award = projectService.getaward(aid)
    awardJson = json.dumps(award, default=award2dict)
    return json.dumps(MessageInfo.success(msg='保存成功',data=awardJson).__dict__)

"""
修改项目接口
"""
@front.route('/api/modifyPro/<int:pid>',methods=['POST'])
def modifyPro(pid):
    data = json.loads(request.get_data(as_text=True))
    projectService.modifyPro(pid,data)
    return json.dumps(MessageInfo.success(msg='保存成功').__dict__)

"""
修改成员信息
"""
@front.route('/api/modifyProMember/<int:mid>',methods=['POST'])
def modifyProMember(mid):
    data = json.loads(request.get_data(as_text=True))
    projectService.modifyProMember(mid,data)
    return json.dumps(MessageInfo.success(msg='保存成功').__dict__)


"""
修改成奖项信息
"""
@front.route('/api/modifyProAward/<int:aid>',methods=['POST'])
def modifyProAward(aid):
    data = json.loads(request.get_data(as_text=True))
    projectService.modifyAwardInfo(aid,data)
    return json.dumps(MessageInfo.success(msg='保存成功').__dict__)


"""
修改项目主页图片
"""
@front.route('/api/modifyMainPic/<int:fid>',methods=['POST'])
def modifyMainPic(fid):
    files = request.files.getlist("pics")
    filename = projectService.modifyPic(fid,files)
    return json.dumps(MessageInfo.success(msg='修改成功',data={
        'url':url_for('common.image', name=filename)
    }).__dict__)

"""
删除成员信息
"""
@front.route('/api/deleteProMember/<int:mid>',methods=['GET'])
def deleteProMember(mid):
    projectService.deleteProMember(mid)
    return json.dumps(MessageInfo.success(msg='删除成功').__dict__)



"""
删除获奖信息
"""
@front.route('/api/deleteProAward/<int:aid>',methods=['GET'])
def deleteProAward(aid):
    projectService.deleteAwardInfo(aid)
    return json.dumps(MessageInfo.success(msg='删除成功').__dict__)

"""
删除文件
"""
@front.route('/api/deleteCertFile/<int:fid>',methods=['GET'])
def deleteCertFile(fid):
    filesService.deleteFileByID(fid)
    return json.dumps(MessageInfo.success(msg='删除成功').__dict__)

"""
上传项目接口
"""
@front.route('/api/uploadProject',methods=['POST'])
def uploadProject():
    #数据
    data = json.loads(request.get_data(as_text=True))
    status = data['status']   # 如果是提交,记录提交的时间
    projectService.addProject(data)
    if status == 2:
        return json.dumps(MessageInfo.success(msg='提交成功').__dict__)
    else:
        return json.dumps(MessageInfo.success(msg='保存成功').__dict__)

"""
项目提交审核
"""
@front.route('/api/submitProject/<int:pid>',methods=['get'])
def submitProject(pid):
    projectService.submitPro(pid)
    return json.dumps(MessageInfo.success(msg='提交成功').__dict__)

"""
导出获奖信息
"""
@front.route('/api/downloadAwardInfo',methods=['GET'])
def downloadAwardInfo():
    startTime = request.args.get('startTime',default=None)
    endTime = request.args.get('endTime', default=None)
    academy = request.args.get('major', default = 0)
    filename = projectService.downProAwardInfo(startTime,endTime,academy)

    return json.dumps(MessageInfo.success(msg='保存成功',data={
        'url': url_for('common.zip', name=filename),
    }).__dict__)


"""
上传项目接口
"""
@front.route('/api/uploadProjectV2',methods=['POST'])
def newuploadProject():
    status = request.form.get("status")
    projectService.addProjectV1(request)
    if status == 2:
        return json.dumps(MessageInfo.success(msg='提交成功').__dict__)
    else:
        return json.dumps(MessageInfo.success(msg='保存成功').__dict__)


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
学生登出接口
"""
@front.route("/api/front/logout", methods=['GET'])
def stu_logout_api():
    session.pop('student', None)
    return redirect(url_for('front.home'))

"""
学生注册接口
"""
@front.route("/api/register",methods=['POST'])
def stu_register_api():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    password = data['password']
    user = User(username,password,3)                    #3代表未验证过的学生
    userService.addUser_v1(user)
    token = base64.b64encode(username.encode())             #用base64加密
    send_mail(username+'@bupt.edu.cn', '账户激活', 'activate', username=username, token=token)
    return json.dumps(MessageInfo.success(msg="请登录北邮人邮箱去验证").__dict__)


"""
激活账户
"""
@front.route("/activate/<token>",methods=['GET'])
def activate(token):
    username = base64.b64decode(token)
    user = userService.selectByName(username,3)
    if user:
        return json.dumps(MessageInfo.success(msg="验证成功").__dict__)
    else:
        return json.dumps(MessageInfo.success(msg="验证错误").__dict__)


"""
学生撤销审核中的项目
"""
@front.route('/api/student/undoPro',methods=['POST'])
def stuUodoPro():
    data = json.loads(request.get_data(as_text=True))
    pid = data["pid"]
    if pid is None:
        return json.dumps(MessageInfo.fail(msg="pid不能为空").__dict__)
    projectService.stuUndoPro(pid)
    return json.dumps(MessageInfo.success(msg="撤销成功").__dict__)
def stuUodoPro():
    data = json.loads(request.get_data(as_text=True))
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
    data = json.loads(request.get_data(as_text=True))
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
    return render_template("tmp01/user.html", pagination=pagination, project=project)

"""
修改项目
"""
@front.route('/student/modifiesProject/<int:pid>')
def modifiesProject(pid):
    project = projectService.getProjectByID(pid)
    return render_template("front/edit-project.html", project=project)

"""
上传项目
"""
@front.route('/student/uploadProject',defaults={'pid':-1})
@front.route('/student/uploadProject/<int:pid>')
def uploadProjectTmp(pid):
    project = []
    if pid!=-1:
        project = projectService.getProjectByID(pid)
    # else:
    #     project = projectService.getProId()
    return render_template("front/edit-project.html", project=project)

"""
新闻列表展示
"""
@front.route('/news', methods=['GET'],defaults={'page':1,'count':10})
@front.route('/news/<int:page>/<int:count>')
def news(page,count):
    pagination, news = newsService.selectByPage(page, count, 3)
    return render_template("front/news.html",pagination=pagination,documents=news)

"""
新闻内容展示
"""
@front.route('/news/detail/<news_id>')
def new(news_id):
    new = newsService.selectByNid(news_id)
    files = filesService.getFilesBySourceIdAndSource(2,news_id)
    return render_template("front/news-detail.html",new=new,files=files)

"""
资料下载展示
"""
@front.route('/downloadfile',defaults={'page':1,'count':10})
@front.route('/downloadfile/<int:page>/<int:count>')
def downloadFile(page,count):
    pagination, files = filesService.getDownloadFile(page, count)
    return render_template("front/downlinks.html", pagination=pagination, files=files)

"""
（查询项目）项目分页展示
"""
@front.route("/projects",methods=['GET'],defaults={'page':1,'count':10})
@front.route("/projects/<int:page>/<int:count>")
def projects(page,count):

    #筛选条件
    startTime = request.args.get('startTime', default=None)
    endTime = request.args.get('endTime', default=None)
    type = request.args.get('type', default=-1, type=int)
    major = request.args.get('major',default=0, type=int)
    source = request.args.get('source',default=-1, type=int)

    pagination,projects = projectService.getPublishedPro(page,count,
                                                         startTime=startTime,
                                                         endTime=endTime,
                                                         type=type,
                                                         major=major,
                                                         source=source)
    return render_template("front/projects.html",projects=projects,pagination=pagination)

"""
项目详细展示
"""
@front.route("/projects/detail",methods=['GET'])
@front.route("/projects/detail/<int:pid>")
def project(pid):
    project = projectService.getProjectByID(pid)
    return render_template("front/project-detail.html",project=project)


"""
项目预览
"""
@front.route("/student/preview/project",methods=['GET'])
@front.route("/student/preview/project/<int:pid>")
def previewProject(pid):
    project = projectService.getProjectByID(pid)
    # return render_template("front/project-preview.html",project=project)
    return render_template("front/project-detail.html",project=project)

"""
基地风采展示
"""
@front.route("/lab")
def lab():
    return render_template("front/lab.html")

@front.route("/lab/i3")
def i3():
    return render_template('tmp01/i3.html')

"""
主页
"""
@front.route("/")
def home():
    # 筛选条件
    startTime = request.args.get('startTime', default=None)
    endTime = request.args.get('endTime', default=None)
    type = request.args.get('type', default=-1, type=int)
    major = request.args.get('major', default=0, type=int)
    source = request.args.get('source', default=-1, type=int)
    pagination,projects = projectService.getPublishedPro(1,4,startTime=startTime,
                                                         endTime=endTime,
                                                         type=type,
                                                         major=major,
                                                         source=source)

    pagination1,news = newsService.selectByPage(1,8,3)
    return render_template("front/home.html",projects=projects,pagination=pagination,news = news)

"""
用户中心
"""
#@front.route("/user/<user_id>")
#def user(user_id):
#    return render_template("tmp01/user2.html") #根据学生的id获取到学生Model

"""
测试用
"""
@front.route("/student",defaults={'page':1,'count':10})
@front.route("/student/<int:page>/<int:count>")
def user(page,count):
    pagination,project = projectService.getProByStudentId(page,count)
    return render_template("front/user.html", pagination=pagination, project=project)

@front.route("/student/login")
def stu_login():
    return render_template("tmp01/login.html")

@front.route("/register")
def stu_register():
    return render_template("tmp01/register.html")
#
# @front.route('/student/manageProject',defaults={'page':1,'count':10})
# @front.route('/student/manageProject/<int:page>/<int:count>')
# def manageProject(page,count):
#     pagination,project = projectService.getProByStudentId(page,count)
#     return render_template("tmp01/user2.html",pagination=pagination,project=project)
