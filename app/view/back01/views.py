#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import datetime
import time



import os
from os import path

from flask import render_template, flash, request, url_for, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename, redirect


from app.view.admin.forms import AddAdminForm, AddProjectForm

import json

from flask import render_template, request

from app.model.models import *
from app.service.ArticleService import *
from app.utils.timeutils import *
from app.view.MessageInfo import MessageInfo
from app.view.back01 import back01
from datetime import datetime


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

@back01.route('/addadmin01', methods=['GET','POST'])
# @login_required
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
def userlist():
    page = request.args.get('page',1,type = int)
    pagination = User.query.order_by(User.created_time.desc()).paginate(page,per_page=15,error_out=False)
    users = pagination.items
    return render_template('admin/edit_user.html',users=users,pagination=pagination)


@back01.route('/delete_user01',methods=['POST'])
@login_required
def delete_user():
    id = request.form.get("id")
    user = User.query.get(id)
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
        # f1= request.files["photo"]
        photos = request.files.getlist('photo')
        # f2 = request.files["video"]
        files = request.files.getlist('video')
        base_path = path.abspath(path.dirname(__file__))
        photoss = []
        video_db_paths = []
        for file in photos:
            print("000000")
            print(allowed_photo(file.filename))
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
        project = Project(pname=form.name.data, introduction=form.introduction.data, teaminfo=str(teaminfo),
                          picture=str(photoPaths), vedio=videoPaths)
        db.session.add(project)
        db.session.commit()

        teammates = []
        flash("保存成功")
    return render_template('back01/addproject.html', form=form, users=teammates)


@back01.route('/adduser01', methods=['GET', 'POST'])
# @login_required
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
# @login_required
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
@back01.route('/query_projects/<project_id>/',methods=['GET', 'POST'])
@login_required
def operate(project_id):
    if  request.form.get("operate") == "编辑":
        print("3333")
        project = Project.query.filter(Project.id == project_id).one()
        form  =AddProjectForm()
        return render_template('admin/editproject.html', project=project, form=form)
    if  request.form.get("operate") == "删除":
        print("4444")
        p = Project.query.filter_by(id=project_id).first()
        db.session.delete(p)
        db.session.commit()
        flash("删除成功")
    projects = Project.query.order_by(Project.create_time.desc()).all()
    return redirect(url_for('admin.query_projects'))
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

@back01.route('/delete/<project_id>/',methods=['GET', 'POST'])
@login_required
def delete(project_id):
    print("4444")
    p = Project.query.filter_by(id=project_id).first()
    db.session.delete(p)
    db.session.commit()
    flash("删除成功")
    projects = Project.query.order_by(Project.create_time.desc()).all()
    return redirect(url_for('back01.query_projects'))
@back01.route('/edit/<project_id>/',methods=['GET', 'POST'])
@login_required
def edit(project_id):
    print("3333")
    project = Project.query.filter(Project.id == project_id).one()
    form  =AddProjectForm()
    return render_template('back01/editproject.html', project=project, form=form)

@back01.route('/addproject01', methods=['GET', 'POST'])
# @login_required
def addproject():
    form = AddProjectForm()
    if form.is_submitted():
        print("555")
        # f1= request.files["photo"]
        photos = request.files.getlist('photo')
        # f2 = request.files["video"]
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


        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
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
    return render_template('back01/article_update.html',article=article)


@back01.route('/back01/lab')
def lab():
    labs = Laboratory.query.order_by(Laboratory.create_time.desc()).all()
    return render_template('back01/lab.html', labs=labs)

@back01.route('/back01/lab/create')
def lab_create():
    return render_template('back01/lab_create.html')

@back01.route('/api/lab/create',methods=['GET','POST'])
def api_create():
    data = json.loads(request.get_data("utf-8"))
    name = data['name']
    intros = data['intros']

    lab = Laboratory(name=name, introduction=intros)
    db.session.add(lab)
    db.session.commit()

    return jsonify({"info": "添加成功"})

@back01.route('/back01/lab/<lab_id>')
def lab_detail(lab_id):
    lab = db.session.query(Laboratory).filter(Laboratory.id == lab_id).one()
    return render_template('back01/lab_detail.html', lab=lab)

@back01.route('/back01/update/<lab_id>')
def lab_update(lab_id):
    lab = db.session.query(Laboratory).filter(Laboratory.id == lab_id).one()
    return render_template('back01/lab_update.html',lab=lab)

@back01.route('/api/lab/update', methods=['POST'])
def api_update():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    name = data['name']
    intros = data['intros']

    lab = db.session.query(Laboratory).filter(Laboratory.id == id).one()
    Laboratory.name = name
    Laboratory.introduction = intros
    db.session.add(lab)
    db.session.commit()

    return jsonify({"info": "修改成功"})

@back01.route('/api/lab/delete',methods=['POST'])
def api_delete():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    lab = db.session.query(Laboratory).filter(Laboratory.id == id).one()
    db.session.delete(lab)
    db.session.commit()

    return jsonify({"info": "删除成功"})



