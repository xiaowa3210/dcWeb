#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import datetime
import time



import os
import uuid
from os import path

from flask import render_template, flash, request, url_for, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename, redirect

from dcwebapp.model.config import UEDITOR_UPLOAD_PATH, HOST
# from app.service.ProjectService import  addProject
from dcwebapp.service.ProjectService import addProject, getProjectById, getTeamInfo, updateProjectByID, getPhotoInfo
from dcwebapp.utils.utils import str_to_dict

from dcwebapp.model.config import STATIC_PATH
from dcwebapp.view.admin.forms import AddAdminForm, AddProjectForm

import json

from flask import render_template, request

from dcwebapp.model.models import *
from dcwebapp.service.ArticleService import *
from dcwebapp.service.LaboratoryService import *
from dcwebapp.utils.timeutils import *
from dcwebapp.view.MessageInfo import MessageInfo
from dcwebapp.view.back01 import back01
from datetime import datetime
from flask import Blueprint, redirect

global a
a=""

global teammates
teammates =[]
global members
members =[]

global activities
activities=[]


PHOTO_ALLOWED_EXTENSIONS = set(['png','jpg','JPG','PNG','gif','GIF'])
VEDIO_ALLOWED_EXTENSIONS= set(['flv','avi','3gp','wmv','rm','rmvb'])
# 用于判断文件后缀
def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in PHOTO_ALLOWED_EXTENSIONS
# 用于判断文件后缀
def allowed_video(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in VEDIO_ALLOWED_EXTENSIONS

@back01.route('/first', methods=['GET'])
@login_required
def first():
    return render_template('back01/index01.html', current_user=current_user)



@back01.route('/addadmin01', methods=['GET','POST'])
@login_required
def addadmin():
    form = AddAdminForm()
    if form.is_submitted():
        print("00000")
        username = form.name.data
        psw1 = form.password.data
        psw2 = form.rep_password.data
        admi = User.query.filter(User.username == username).first()
        if admi:
            print("111111")
            flash("用户名已经存在")
        elif psw1 != psw2:
            print("22222")
            flash("两次密码不一致")
        else:
            admin = User(username=form.name.data, pwd=form.password.data)
            db.session.add(admin)
            db.session.commit()
            print("33333333")
            flash("保存成功")
            # return render_template('index0000000.html')
    # return render_template('index0000000.html')
    return render_template('back01/addadmin.html',form=form)
"""
**********************************
"""
@back01.route('/userlist01')
@login_required
def userlist01():
    page = request.args.get('page',1,type = int)
    pagination = User.query.order_by(User.created_time.desc()).paginate(page,per_page=10,error_out=False)
    users = pagination.items
    return render_template('back01/edit_user01.html',users=users,pagination=pagination)





@back01.route('/deluser',methods=['POST'])
def deluser():
    print("*********************************")
    data = int(json.loads(request.get_data("utf-8")))
    print(data)
    print(type(data))

    print("*********************************")
    user = User.query.get(data)
    print(user)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'code':200,'message':'删除成功！'})

@back01.route('/addproject00', methods=['GET', 'POST'])
# @login_required
def addt_project():
    form = AddProjectForm()

    # print(request.form.get("adduser"))
    # if request.form.get("adduser") == "+":
    #     print("3e764354")
    #     print(form.name.data)
    #     global a
    #     a = form.name.data
    #     return render_template('admin/users.html')
    # if request.form.get("submit") == "adduser":
    #     username =request.form.get("username")
    #     pro = request.form.get("pro")
    #     grade = request.form.get("grade")
    #     teammate = {"name":username,"faculty":pro,"grade":grade}
    #     global  teammates
    #     teammates.append(teammate)
    #     flash("保存成功")
    #     form.name.data = a
    #     print(form.name.data)
    #     return render_template('admin/addproject.html', form=form, users=teammates)
    # if request.method == 'POST':
    if form.is_submitted():
        print("555")
        # f1= request.resources["photo"]
        photos = request.files.getlist('photo')
        # f2 = request.resources["video"]
        files = request.files.getlist('video')
        base_path = path.abspath(path.dirname(__file__))
        photoss = []
        video_db_paths = []
        for file in photos:
            print("000000")
            print(allowed_photo(file.filename))
            if allowed_photo(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(STATIC_PATH, 'img', filename)
                photo = {"title": filename, "path": 'img/' + filename}
                file.save(upload_path)
                photoss.append(photo)
            else:
                flash("您上传的文件不是图片类型！")
                return render_template('admin/addproject.html', form=form)
        for file in files:
            if allowed_video(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                video_db_paths.append(upload_path)
                file.save(upload_path)
            else:
                flash("您上传的文件不是视频类型！")
                return render_template('admin/addproject.html', form=form)
        # print("22222222" + photos)
        photoPaths = {"pics": photoss}
        # print("33333" + photoPaths)

        videoPaths = ";".join(video_db_paths)
        global teammates

        # upload_path = path.join(base_path, 'uploads/')
        # print(upload_path)
        # file_name1 = upload_path + secure_filename(f1.filename)
        # f1.save(file_name1)
        # file_name2 = upload_path + secure_filename(f2.filename)
        # f2.save(file_name2)
        teaminfo = {"teammates": teammates}
        print("34222222222")
        print(teaminfo)
        print(photoPaths)
        project = Project(pname=form.name.data, introduction=form.introduction.data, teaminfo=json.dumps(teaminfo),
                          picture=str(photoPaths), vedio=videoPaths)
        db.session.add(project)
        db.session.commit()

        teammates = []
        flash("保存成功")
    return render_template('back01/addproject.html', form=form, users=teammates)


@back01.route('/adduser01', methods=['GET', 'POST'])
@login_required
def adduser():
    form = AddProjectForm()
    if form.is_submitted():
        username = request.form.get("name")
        faculty = request.form.get("faculty")
        grade = request.form.get("grade")
        teammate = {"name": username,
                    "faculty": faculty,
                    "grade": grade}
        teammates.append(teammate)
        # flash("保存成功")
        return render_template('back01/addproject.html', form=AddProjectForm(), users=teammates)

    return render_template('back01/users.html', form=form)
@back01.route('/query_projects01', methods=['GET','POST'])
@login_required
def query_projects():
    # projects = Project.query.order_by(Project.create_time.desc()).all()
    # return render_template('admin/projects.html', projects=projects)

   # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page',1))
    # 获取get请求传过来的以多少条数据分页的参数，默认为5
    per_page = int(request.args.get('per_page',7))
    paginate = nProject.query.order_by(nProject.create_time.desc()).paginate(page, per_page, error_out=False)
    # paginate = Project.query.order_by(Project.create_time.desc()).paginate(page, per_page, error_out=False)
    # 获得数据
    projects = paginate.items
    # 返回给前端
    return render_template('back01/projects.html', paginate=paginate, projects=projects)

@back01.route('/projects01/<project_id>/',methods=['GET', 'POST'])
@login_required
def pdetail(project_id):
    return redirect(url_for('tmp05.projects_detail',project_id=project_id))
    # project_obj = getProjectById(project_id)
    # teammates,honors = getTeamInfo(project_obj)
    # return render_template('tmp05/projects-detail.html',
    #                        project=project_obj,
    #                        teammates=teammates,
    #                        honors=honors)
    # project = Project.query.filter(Project.id == project_id).one()
    # return render_template('tmp00/pdetail.html', project=project)

@back01.route('/delete01/<project_id>/',methods=['GET', 'POST'])
@login_required
def delete(project_id):
    p = nProject.query.filter_by(project_id=project_id).first()
    # p = Project.query.filter_by(id=project_id).first()
    db.session.delete(p)
    db.session.commit()
    flash("删除成功")
    # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page', 1))
    # 获取get请求传过来的以多少条数据分页的参数，默认为5
    per_page = int(request.args.get('per_page', 7))
    paginate = nProject.query.order_by(nProject.create_time.desc()).paginate(page, per_page, error_out=False)
    # paginate = Project.query.order_by(Project.create_time.desc()).paginate(page, per_page, error_out=False)
    # 获得数据
    projects = paginate.items
    # 返回给前端
    return render_template('back01/projects.html', paginate=paginate, projects=projects)
@back01.route('/project/Modified', methods=['GET'])
@login_required
def projectModified():
    project_id = request.values.get("project_id")
    project= getProjectById(project_id)
    print("8374834")
    print(project.ban_url)
    teammates= getTeamInfo(project)
    photos =getPhotoInfo(project)
    # kws = kwsStr.split("||")
    return render_template('back01/editproject.html', project=project,teammates=teammates,photos=photos)

@back01.route('/edit01/<project_id>/',methods=['GET', 'POST'])
@login_required
def edit(project_id):
    print("3333")
    project = nProject.query.filter(nProject.project_id == project_id).one()
    teammates = str_to_dict(project.member_info)
    teammates =teammates['teammates']
    form  =AddProjectForm()
    print(project.member_info)
    # users =project.member_info["teammates"].split(',')
    if form.is_submitted():
        print("555")
        # f1= request.resources["photo"]
        photos = request.files.getlist('photo')
        # f2 = request.resources["video"]
        files = request.files.getlist('video')
        base_path = path.abspath(path.dirname(__file__))
        photoss = []
        video_db_paths = []
        for file in photos:
            if allowed_photo(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                photo = {"title": filename, "path": upload_path}
                file.save(upload_path)
                photoss.append(photo)
            else:
                flash("您上传的文件不是图片类型！")
                return render_template('admin/addproject.html', form=form)
        for file in files:
            if allowed_video(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                video_db_paths.append(upload_path)
                file.save(upload_path)
            else:
                flash("您上传的文件不是视频类型！")
                return render_template('admin/addproject.html', form=form)

        photoPaths = {"pics": photoss}

        videoPaths = ";".join(video_db_paths)
        # global teammates

        teaminfo = {"teammates": teammates}
        t = time.time()
        print(t)  # 原始时间数据
        print(int(t))  # 秒级时间戳
        tr = int(round((t*1000)))
        print(tr)  # 毫秒级时间戳

        nowTime = lambda: int(round(t * 1000))
        print(nowTime());  # 毫秒级时间戳，基于lambda

        if(form.isPublish.data):
            publish_flag = 1
        else:
            publish_flag = 0


        project= nProject.query.filter(nProject.project_id == project_id).one()
        print(project)
        print(type(project))
        project.title = form.name.data
        project.brief = form.introduction.data
        project.member_info = str(teaminfo)
        # project = Project(pname = form.name.data,introduction =form.introduction.data,picture=photoPaths,vedio=videoPaths)
        # db.session.add(project)
        db.session.commit()

        teammates = []
        flash("修改成功")
        # 获取get请求传过来的页数,没有传参数，默认为1
        page = int(request.args.get('page', 1))
        # 获取get请求传过来的以多少条数据分页的参数，默认为5
        per_page = int(request.args.get('per_page', 7))
        paginate = nProject.query.order_by(nProject.create_time.desc()).paginate(page, per_page, error_out=False)
        # paginate = Project.query.order_by(Project.create_time.desc()).paginate(page, per_page, error_out=False)
        # 获得数据
        projects = paginate.items
        # 返回给前端
        return render_template('back01/projects.html', paginate=paginate, projects=projects)

    return render_template('back01/editproject.html', project=project, teammates=teammates)

@back01.route('/addproject01', methods=['GET', 'POST'])
@login_required
def addproject():
    form = AddProjectForm()
    if form.is_submitted():
        print("555")
        # f1= request.resources["photo"]
        photos = request.files.getlist('photo')
        # f2 = request.resources["video"]
        files = request.files.getlist('video')
        base_path = path.abspath(path.dirname(__file__))
        photoss = []
        video_db_paths = []
        for file in photos:
            if allowed_photo(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                print(upload_path)
                photo = {"title": filename, "path": upload_path}
                file.save(upload_path)
                photoss.append(photo)
            else:
                flash("您上传的文件不是图片类型！")
                return render_template('admin/addproject.html', form=form)
        for file in files:
            if allowed_video(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                video_db_paths.append(upload_path)
                file.save(upload_path)
            else:
                flash("您上传的文件不是视频类型！")
                return render_template('admin/addproject.html', form=form)

        photoPaths = {"pics": photoss}

        videoPaths = ";".join(video_db_paths)
        global teammates

        teaminfo = {"teammates": teammates}
        t = time.time()
        print(t)  # 原始时间数据
        print(int(t))  # 秒级时间戳
        tr = int(round((t*1000)))
        print(tr)  # 毫秒级时间戳

        nowTime = lambda: int(round(t * 1000))
        print(nowTime());  # 毫秒级时间戳，基于lambda

        print("2222222")
        print(form.isPublish.data)
        print(type(form.isPublish.data))
        if(form.isPublish.data):
            publish_flag = 1
        else:
            publish_flag = 0


        nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        project = nProject(project_id = str(tr),title=form.name.data, brief=form.introduction.data, member_info=str(teaminfo),
                           ban_url=str(photoPaths),delete_flag=0,publish_flag=publish_flag,modified_flag=0,create_time=nowTime,publish_time=nowTime,broad_time=nowTime,creator_id=1)
        db.session.add(project)
        db.session.commit()

        teammates = []
        flash("保存成功")
    return render_template('back01/addproject.html', form=form, users=teammates)


@back01.route('/back01/updateArticle/<string:article_id>', methods=['GET'])
def updateArticle(article_id):
    article = getArticleByID(article_id)
    return render_template('back01/back/rticle_modified.html',article=article)





@back01.route('/saveProject', methods=['POST'])
@login_required
def saveProject():
    # 解析前端传过来的json数据
    # data = json.loads(request.get_data("utf-8"))

    #attachment = request.resources.get("attachment")

    photos = request.files.getlist("photos")
    # is_attachment = 1
    # resources = []

    photoss = []
    if len(photos) > 0:
        # is_attachment = 0
        path = UEDITOR_UPLOAD_PATH + "/project_photo/"
        if not os.path.exists(path):
            os.mkdir(path)
        for file in photos:
            if allowed_photo(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(path,  filename)
                photo = {"title": filename, "path": upload_path}
                file.save(upload_path)
                photoss.append(photo)
            else:
                flash("您上传的文件不是图片类型！")
    photoPaths = {"pics": photoss}
    title = request.form.get("title")
    # subtitle = request.form.get('subtitle')
    brief = request.form.get('brief')

    teammates =request.form.get('teammates')
    teammates = teammates.split("&")
    member_infos=[]
    for teammate in  teammates:
        ada = teammate.strip(',').split('||')

        name = ada[0]
        faculty = ada[1]
        grade = ada[2]
        teammate = {"name": name,
                    "faculty": faculty,
                    "grade": grade}
        member_infos.append(teammate)
        # print(type(ada))

    member_info ={"teammates": member_infos}
    print(str(member_info))

    # keywords = request.form.get('kws')
    # content = request.form.get('content')
    is_add = request.form.get('is_add')
    type = request.form.get('type')
    # 添加文章
    if is_add == '0':
         # 0代表保存，1代表保存并且发布
        project = nProject()

        t = time.time()
        tr = int(round((t*1000)))
        project.project_id = 'Project' + str(tr)
        project.title = title
        project.brief=brief
        project.member_info =str(member_info)
        project.ban_url =str(photoPaths)
        project.delete_flag =0
        project.modified_flag=0
        project.create_time =datetime.now()
        project.publish_time =datetime.now()
        project.broad_time=datetime.now()
        project.creator_id=1

        if type == '1':
            project.publish_flag=1
        else:
            project.publish_flag = 0

        #如果有附件

        if addProject(project):
            return json.dumps(MessageInfo.success(data='保存成功').__dict__)
        else:
            return json.dumps(MessageInfo.fail(data="保存失败").__dict__)
    else:
        # 修改文章
        project = nProject()
        project.project_id = request.form.get('project_id')
        project.title = title
        project.brief = brief
        project.member_info = str(member_info)
        project.ban_url =str(photoPaths)

        if type == '1':
            project.publish_flag = 1  # 设置为已发布
            project.publish_id = project.creator_id  # 发布人id就是创建人id
            project.publish_time = datetime.now()
        if updateProjectByID(project):
            return json.dumps(MessageInfo.success(data='修改成功').__dict__)
        else:
            return json.dumps(MessageInfo.fail(data="修改失败").__dict__)
@back01.route('/deletePhoto', methods=['GET','POST'])
@login_required
def deletePhotoById():
     #解析前端传过来的json数据
    # data = json.loads(request.get_data("utf-8"))
    data = json.loads(request.get_data().decode("utf-8"))
    project_id = data["project_id"]
    project = getProjectById(project_id)
    file_id = data["file_id"]
    file_path = data["file_path"]
    project = getProjectById(project_id)
    pics = getPhotoInfo(project)
    photo = {"title": file_id, "path": file_path}
    pics.remove(photo)
    photoPaths = {"pics": pics}
    project.ban_url =str(photoPaths)
    db.session.commit()
    if deletePhoto(file_id,file_path):
        return json.dumps(MessageInfo.success(data='图片删除成功').__dict__)
    else:
        return json.dumps(MessageInfo.fail(data="图片删除失败").__dict__)

def deletePhoto(file_id,file_path):

    if os.path.exists(file_path):
        os.remove(file_path)
    return True



