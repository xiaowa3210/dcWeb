# from backstage import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
# from backstage import utils
# from backstage.models import CfgNotify
# from backstage.tmp01.forms import CfgNotifyForm
from app.models import Document, Project,User, db
from app.view.backstage import utils
from app.view.backstage.main.forms import AddinfoForm, AddDocumentForm, AddProjectForm, AddAdminForm

from . import main
from flask import Flask, request,make_response,render_template, redirect, url_for
from werkzeug.utils import secure_filename # 使用这个是为了确保filename是安全的
from os import path


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


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# # 根目录跳转
# @tmp01.route('/', methods=['GET'])
# @login_required
# def root():
#     return redirect(url_for('tmp01.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('backapp/index.html', current_user=current_user)

@main.route('/addadmin', methods=['GET','POST'])
# @login_required
def addadmin():
    form = AddAdminForm()
    if form.is_submitted():
        username = form.name.data
        psw1 = form.password.data
        psw2 = form.rep_password.data
        admi = User.query.filter(User.username == username).first()
        if admi:
            flash("用户名已经存在")
        elif psw1 != psw2:
            flash("两次密码不一致")
        else:
            admin = User(username=form.name.data, password=form.password.data)
            db.session.add(admin)
            db.session.commit()
            flash("保存成功")
    return render_template('backapp/addadmin.html', form=form)



#添加信息页

@main.route('/addinfo', methods=['GET','POST'])
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

    return render_template('backapp/addinfo.html', form=form)

@main.route('/addproject', methods=['GET','POST'])
@login_required
def addproject():
    form = AddProjectForm()
    if form.is_submitted():

        if request.method == 'POST':
            print("555")
            f1= request.files["photo"]
            f2 = request.files["video"]
            base_path = path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path, 'uploads/')
            print(upload_path)
            file_name1 = upload_path + secure_filename(f1.filename)
            f1.save(file_name1)
            file_name2 = upload_path + secure_filename(f2.filename)
            f2.save(file_name2)
        project = Project(pname = form.name.data,introduction =form.introduction.data,picture=file_name1,vedio=file_name2)
        db.session.add(project)
        db.session.commit()
        flash("保存成功")
    return render_template('backapp/addproject.html', form=form)
@main.route('/query_projects', methods=['GET','POST'])
@login_required
def query_projects():

    # cc = Project()
    # cc.pname = ('hhh')
    # cc.introduction = ('jj')
    # db.session.add(cc)
    # db.session.commit()

    projects = Project.query.order_by(Project.create_time.desc()).all()
    for project in projects:
        print(project.pname)
    if request.method== 'POST':
        pid = request.form.get("")
    print(projects)
    return render_template('backapp/projects.html', projects=projects)
@main.route('/query_projects/<project_id>/',methods=['GET', 'POST'])
def operate(project_id):
    if  request.form.get("operate") == "编辑":
        print("3333")
        project = Project.query.filter(Project.id == project_id).one()
        form  =AddProjectForm()
        return render_template('backapp/editproject.html', project=project,form=form)
    if  request.form.get("operate") == "删除":
        print("4444")
        p = Project.query.filter_by(id=project_id).first()
        db.session.delete(p)
        db.session.commit()
        flash("删除成功")
    projects = Project.query.order_by(Project.create_time.desc()).all()
    return render_template('backapp/projects.html', projects=projects)
@main.route('/projects/<project_id>/',methods=['GET', 'POST'])
def pdetail(project_id):
    project = Project.query.filter(Project.id == project_id).one()
    return render_template('projectview/pdetail.html', project=project)







@main.route('/addpolicy', methods=['GET','POST'])
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
    return render_template('backapp/addpolicy.html', form=form)