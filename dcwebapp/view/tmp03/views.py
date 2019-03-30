#!/user/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template

from dcwebapp.service.DocumentsService import *
from dcwebapp.service.ProjectService import *
from dcwebapp.view.tmp03 import tmp03


@tmp03.route('/tmp03')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(10)
    projects = Project.query.order_by(Project.create_time.desc()).limit(3)
    return render_template('tmp03/home02.html', projects=projects, documents=documents)

@tmp03.route('/tmp03/login')
def login():
    pass

@tmp03.route('/tmp03/register')
def register():
    pass

@tmp03.route('/tmp03/logout')
def logout():
    pass

@tmp03.route('/tmp03/user')
def user_center():
    pass

@tmp03.route('/tmp03/news', defaults={'page':1})
@tmp03.route('/tmp03/news/<int:page>')
def news(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 1)
    return render_template('tmp03/news.html', pagination=pagination, documents=documents)

@tmp03.route('/tmp03/newsDetail/<news_id>')
def news_detail(news_id):
    news_obj = getDoucumentByID(news_id)
    return render_template('tmp03/news_detail.html', news=news_obj)

@tmp03.route('/tmp03/downlink', defaults={'page':1})
@tmp03.route('/tmp03/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 0)
    return render_template('tmp03/downlink.html', pagination=pagination, documents=documents)

#文件下载
# @tmp03.route('/tmp03/download/<string:filename>', methods=['GET'])
# def download_file(filename):
#     #需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     directory = os.path.join(app.root_path, 'view/admin/uploads')
#     response = make_response(send_from_directory(directory, filename, as_attachment=True))
#     response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
#     return response

@tmp03.route('/tmp03/projects', defaults={'page':1})
@tmp03.route('/tmp03/projects/<int:page>')
def projects(page):
    per_page = 3
    pagination,projects = getProjectsByPage(page, per_page)
    return render_template('tmp03/projects.html', pagination=pagination, projects=projects)

@tmp03.route('/tmp03/projectdetail/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    teammates,honors = getTeamInfo(project_obj)
    return render_template('tmp03/projects_detail.html',
                           project=project_obj,
                           teammates=teammates,
                           honors=honors)


@tmp03.route('/tmp03/pDetail')
def pDetail():
    return render_template('tmp03/projects_detail.html')

@tmp03.route('/tmp03/lib')
def lib():
    return render_template('tmp03/lib.html')

@tmp03.route('/tmp03/contact')
def contact():
    return render_template('tmp03/contact.html')