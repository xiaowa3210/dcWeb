#!usr/bin/python
# -*- coding: utf-8 -*-

# from backstage import get_logger, get_config
import os
from os import path

from app.view.admin import admin
from flask import flash
from flask import request, render_template, redirect, url_for,jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename  # 使用这个是为了确保filename是安全的

# from backstage import utils
# from backstage.models import CfgNotify
# from backstage.tmp01.forms import CfgNotifyForm
from app.models import Document, Project, User, db, Laboratory, Activity
from app.view.admin.forms import AddinfoForm, AddDocumentForm, AddProjectForm, AddAdminForm, AddMemberForm, AddLabForm, \
    AddActivityForm

global a
a=""

global teammates
teammates =[]
global members
members =[]

global activities
activities=[]




# logger = get_logger(__name__)
# cfg = get_config()

# 通用列表查询
# def common_list(DynamicModel, view):
#     # 接收参数
#     action = request.args.get('action')
#     id = request.args.get('id')
#     page = int(request.args.get('page')) if request.args.get('page') else 1
#     length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE
#
#     # 删除操作
#     if action == 'del' and id:
#         try:
#             DynamicModel.get(DynamicModel.id == id).delete_instance()
#             flash('删除成功')
#         except:
#             flash('删除失败')
#
#     # 查询列表
#     query = DynamicModel.select()
#     total_count = query.count()
#
#     # 处理分页
#     if page: query = query.paginate(page, length)
#
#     dict = {'content': utils.query_to_list(query), 'total_count': total_count,
#             'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
#     return render_template(view, form=dict, current_user=current_user)
PHOTO_ALLOWED_EXTENSIONS = set(['png','jpg','JPG','PNG','gif','GIF'])
VEDIO_ALLOWED_EXTENSIONS= set(['flv','avi','3gp','wmv','rm','rmvb'])
# 用于判断文件后缀
def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in PHOTO_ALLOWED_EXTENSIONS
# 用于判断文件后缀
def allowed_video(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in VEDIO_ALLOWED_EXTENSIONS


# # 根目录跳转
# @tmp01.route('/', methods=['GET'])
# @login_required
# def root():
#     return redirect(url_for('tmp01.index'))


# 首页
@admin.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('admin/index.html', current_user=current_user)


@admin.route('/addadmin', methods=['GET','POST'])
@login_required
def addadmin():
    form = AddAdminForm()
    if form.is_submitted():
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
    return render_template('admin/addadmin.html', form=form)



#添加信息页

@admin.route('/addinfo', methods=['GET','POST'])
@login_required
def addinfo():
    form = AddinfoForm()
    if form.is_submitted():
        print("2333332")
        if request.method == 'POST':
            print("555")
            f = request.files["attachment"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path, 'uploads/')
            print(upload_path)
            file_name = upload_path + secure_filename(f.filename)
            f.save(file_name)
        info = Document(title = form.title.data,content = form.content.data,attachment=upload_path)
        db.session.add(info)
        db.session.commit()
        flash("保存成功")

    return render_template('admin/addinfo.html', form=form)



"""
*********************************************************
*********************************************************
"""

@admin.route('/upload_news',methods=['GET','POST'])
@login_required
def upload_news():
    if request.method == 'GET':
        return render_template('admin/addinfo.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        print("*"*40)
        print(title)
        print(content)
        new_info = Document(title=title,content=content,type=1)
        db.session.add(new_info)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '数据保存成功'})


@admin.route('/backnews')
@login_required
def backnews():
    page = request.args.get('page',1,type = int)
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page,per_page=15,error_out=False)
    documents = pagination.items
    return render_template('admin/backnews.html',documents=documents,pagination=pagination)

@admin.route('/backnews_detail/<document_id>')
@login_required
def backnews_detail(document_id):
    documents = Document.query.filter(Document.id == document_id).first()
    return render_template('tmp01/news-detail.html',news = documents)

@admin.route('/editinfo/<news_id>',methods=['GET','POST'])
@login_required
def editinfo(news_id):
    if request.method ==  'GET':
        news_obj = Document.query.get(news_id)
    return render_template('admin/editinfo.html',news=news_obj)

@admin.route('/delete_news',methods=['POST'])
@login_required
def delete_news():
    id = request.form.get("id")
    document = Document.query.get(id)
    db.session.delete(document)
    db.session.commit()
    return jsonify({'code':200,'message':'删除成功！'})








@admin.route('/addproject', methods=['GET','POST'])
@login_required
def addproject():
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
        print(path.dirname(__file__))
        print(base_path.split("app")[-2] + "upload")
        base_path = base_path.split("app")[-2]
        photoss = []
        video_db_paths = []
        for file in photos:
            print("000000")
            print(allowed_photo(file.filename))
            if allowed_photo(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                photo= {"title":filename,"path":upload_path}
                file.save(upload_path)
                photoss.append(photo)
            else:
                flash("您上传的文件不是图片类型！")
                return render_template('admin/addproject.html', form=form)
        for file in files:
            if  allowed_video(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                video_db_paths.append(upload_path)
                file.save(upload_path)
            else:
                flash("您上传的文件不是视频类型！")
                return render_template('admin/addproject.html', form=form)
        # print("22222222" + photos)
        photoPaths={"pics":photoss}
        # print("33333" + photoPaths)


        videoPaths=";".join(video_db_paths)
        global teammates

            # upload_path = path.join(base_path, 'uploads/')
            # print(upload_path)
            # file_name1 = upload_path + secure_filename(f1.filename)
            # f1.save(file_name1)
            # file_name2 = upload_path + secure_filename(f2.filename)
            # f2.save(file_name2)
        teaminfo = {"teammates":teammates}
        print("34222222222")
        print(teaminfo)
        print(photoPaths)
        project = Project(pname = form.name.data,introduction =form.introduction.data,teaminfo=str(teaminfo),picture= str(photoPaths),vedio=videoPaths)
        db.session.add(project)
        db.session.commit()
        
        teammates =[]

        flash("保存成功")
    return render_template('admin/addproject.html', form=form, users=teammates)

@admin.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    form = AddProjectForm()
    if form.is_submitted():
        username =request.form.get("name")
        faculty =request.form.get("faculty")
        grade = request.form.get("grade")
        teammate = {  "name": username,
          "faculty": faculty,
          "grade": grade}
        teammates.append(teammate)
        flash("保存成功")
        return render_template('admin/addproject.html', form=AddProjectForm(), users=teammates)

    return render_template('admin/users.html', form=form)

@admin.route('/editproject/<project_id>/', methods=['GET','POST'])
@login_required
def editproject(project_id):
    form = AddProjectForm()
    if form.is_submitted():
        if request.method == 'POST':
            print("555")
            # f1= request.files["photo"]
            photos = request.files.getlist('photo')
            # f2 = request.files["video"]
            files = request.files.getlist('video')
            base_path = path.abspath(path.dirname(__file__))
            photo_db_paths = []
            video_db_paths = []
            for file in photos:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                photo_db_paths.append(upload_path)
                file.save(upload_path)
            for file in files:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(base_path, 'uploads', filename)
                video_db_paths.append(upload_path)
                file.save(upload_path)
            photoPaths=";".join(photo_db_paths)
            videoPaths=";".join(video_db_paths)
        project  = Project.query.filter(Project.id == project_id).one()
        print(project)
        print(type(project))
        project.pname =  form.name.data
        project.introduction =form.introduction.data
        project.picture = photoPaths
        project.vedio = videoPaths
        # project = Project(pname = form.name.data,introduction =form.introduction.data,picture=photoPaths,vedio=videoPaths)
        # db.session.add(project)
        db.session.commit()
        flash("保存成功")
    return redirect(url_for('admin.query_projects'))

@admin.route('/query_projects', methods=['GET','POST'])
@login_required
def query_projects():
    # projects = Project.query.order_by(Project.create_time.desc()).all()
    # return render_template('admin/projects.html', projects=projects)

   # 获取get请求传过来的页数,没有传参数，默认为1
    page = int(request.args.get('page',1))
    # 获取get请求传过来的以多少条数据分页的参数，默认为5
    per_page = int(request.args.get('per_page',7))
    paginate = Project.query.order_by(Project.create_time.desc()).paginate(page, per_page, error_out=False)
    # 获得数据
    projects = paginate.items
    # 返回给前端
    return render_template('admin/projects.html', paginate=paginate, projects=projects)

@admin.route('/query_projects/<project_id>/',methods=['GET', 'POST'])
@login_required
def operate(project_id):
    if  request.form.get("operate") == "编辑":
        print("3333")
        project = Project.query.filter(Project.id==project_id).one()
        form  =AddProjectForm()
        return render_template('admin/editproject.html',project=project,form=form)
    if  request.form.get("operate") == "删除":
        print("4444")
        p = Project.query.filter_by(id=project_id).first()
        db.session.delete(p)
        db.session.commit()
        flash("删除成功")
    projects = Project.query.order_by(Project.create_time.desc()).all()
    return redirect(url_for('admin.query_projects'))

@admin.route('/projects/<project_id>/',methods=['GET', 'POST'])
@login_required
def pdetail(project_id):
    project = Project.query.filter(Project.id == project_id).one()
    return render_template('main/../templates/tmp00/pdetail.html', project=project)

@admin.route('/addpolicy', methods=['GET','POST'])
@login_required
def addpolicy():
    print("35657")
    form = AddDocumentForm()
    if form.is_submitted():
        if request.method == 'POST':
            print("555")
            f = request.files["attachment"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path, 'uploads/')
            print(upload_path)
            file_name = upload_path + secure_filename(f.filename)
            f.save(file_name)
        document = Document(title = form.title.data,link = upload_path)
        db.session.add(document)
        db.session.commit()
        flash("保存成功")
    return render_template('admin/addpolicy.html', form=form)
@admin.route('/addmember', methods=['GET','POST'])
@login_required
def addmember():
    mform = AddMemberForm()
    form = AddLabForm()
    # if request.method == 'POST':
    #     form = request.form
    #     print ("6666666")
    #     print (form)
    if mform.is_submitted():
        username = request.form.get("username")
        pro = request.form.get("pro")
        intro = request.form.get("introduction")
        member = {"name": username, "title": pro, "introductin": intro}
        global members
        members.append(member)
        return render_template('admin/addlab.html',form = form,users=members)
    return render_template('admin/addmember.html',form=mform)

@admin.route('/addlab', methods=['GET','POST'])
@login_required
def addlab():
    form = AddLabForm()
    global members
    m = {"members":members}
    if form.is_submitted():
        global activities
        lab = Laboratory(name =form.name.data,introduction =form.introduction.data,member=str(m),activities=activities)
        db.session.add(lab)
        db.session.commit()
        activities =[]
     
        members=[]

        teammates=[]
        flash("保存成功")
    return render_template('admin/addlab.html', form=form,users=members,activities=activities)


@admin.route('/addactivity', methods=['GET','POST'])
@login_required
def addactivity():
    aform = AddActivityForm()
    if aform.is_submitted():
        activity = Activity(title=aform.name.data,content=aform.introduction.data)
        global activities
        activities.append(activity)
        return render_template('admin/addlab.html', form=AddLabForm(), users=members,activities=activities)
    return render_template('admin/addactivity.html', form=aform)











