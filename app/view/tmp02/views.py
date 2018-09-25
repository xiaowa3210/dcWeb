#!/user/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template

from app.service.DocumentsService import *
from app.service.ProjectService import *
from app.view.tmp02 import tmp02


@tmp02.route('/tmp02')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(10)
    projects = Project.query.order_by(Project.create_time.desc()).limit(4)
    return render_template('tmp02/home02.html', projects=projects, documents=documents)

@tmp02.route('/tmp02/login')
def login():
    pass

@tmp02.route('/tmp02/register')
def register():
    pass

@tmp02.route('/tmp02/logout')
def logout():
    pass

@tmp02.route('/tmp02/user')
def user_center():
    pass

@tmp02.route('/tmp02/news', defaults={'page':1})
@tmp02.route('/tmp02/news/<int:page>')
def news(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 1)
    return render_template('tmp02/news.html', pagination=pagination, documents=documents)

@tmp02.route('/tmp02/newsDetail/<news_id>')
def news_detail(news_id):
    news_obj = getDoucumentByID(news_id)
    return render_template('tmp02/news_detail.html', news=news_obj)

@tmp02.route('/tmp02/downlink', defaults={'page':1})
@tmp02.route('/tmp02/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 0)
    return render_template('tmp02/downlink.html', pagination=pagination, documents=documents)

#文件下载
# @tmp02.route('/tmp02/download/<string:filename>', methods=['GET'])
# def download_file(filename):
#     #需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
#     directory = os.path.join(app.root_path, 'view/admin/uploads')
#     response = make_response(send_from_directory(directory, filename, as_attachment=True))
#     response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
#     return response

@tmp02.route('/tmp02/projects', defaults={'page':1})
@tmp02.route('/tmp02/projects/<int:page>')
def projects(page):
    per_page = 3
    pagination,projects = getProjectsByPage(page, per_page)
    return render_template('tmp02/projects.html', pagination=pagination, projects=projects)

@tmp02.route('/tmp02/projectdetail/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    teammates,honors = getTeamInfo(project_obj)
    return render_template('tmp02/projects_detail.html',
                           project=project_obj,
                           teammates=teammates,
                           honors=honors)


@tmp02.route('/tmp02/lib')
def lib():
    return render_template('tmp02/lib.html')

@tmp02.route('/tmp02/contact')
def contact():
    return render_template('tmp02/contact.html')