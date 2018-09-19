#!/user/bin/env python
# -*- coding:utf-8 -*-
import os
from flask import render_template, make_response, send_from_directory

from app.service.DocumentsService import *
from app.service.ProjectService import *
from app.service.LaboratoryService import *
from app.view.tmp05 import tmp05

from app import app


@tmp05.route('/tmp05')
def home():
    # documents = Document.query.order_by(Document.created_time.desc()).limit(6)
    # projects = Project.query.order_by(Project.create_time.desc()).limit(3)
    return render_template('tmp05/home.html')

@tmp05.route('/tmp05/login')
def login():
    pass

@tmp05.route('/tmp05/register')
def register():
    pass

@tmp05.route('/tmp05/logout')
def logout():
    pass

@tmp05.route('/tmp05/user')
def user_center():
    pass

@tmp05.route('/tmp05/news', defaults={'page':1})
@tmp05.route('/tmp05/news/<int:page>')
def news(page):
    per_page = 10
    pagination,documents = getDocumentByPage(page,per_page,1)
    return render_template('tmp05/news.html', pagination=pagination, documents=documents)

@tmp05.route('/tmp05/news/detail/<news_id>')
def news_detail(news_id):
    news_obj = getDoucumentByID(news_id)
    return render_template('tmp05/news-detail.html', news=news_obj)

@tmp05.route('/tmp05/downlink', defaults={'page':1})
@tmp05.route('/tmp05/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 0)
    return render_template('tmp05/downlink.html', pagination=pagination, documents=documents)

#文件下载
@tmp05.route('/tmp05/download/<string:filename>', methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(app.root_path, 'app/view/admin/uploads')
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@tmp05.route('/tmp05/projects', defaults={'page':1})
@tmp05.route('/tmp05/projects/<int:page>')
def projects(page):
    per_page = 3
    pagination,projects = getProjectsByPage(page,per_page)
    return render_template('tmp05/projects.html', pagination=pagination, projects=projects)

@tmp05.route('/tmp05/projectdetail/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    teammates,honors = getTeamInfo(project_obj)
    return render_template('tmp05/projects-detail.html',
                           project=project_obj,
                           teammates=teammates,
                           honors=honors)

@tmp05.route('/tmp05/laboratorys', defaults={'page':1})
@tmp05.route('/tmp05/laboratorys/<int:page>')
def laboratorys(page):
    per_page = 3
    pagination,labs = getLaboratoryByPage(page,per_page)
    return render_template('tmp05/laboratory.html', pagination=pagination, labs=labs)

@tmp05.route('/tmp05/labIntroduction/<lab_id>')
def laboratoryIntroduction(lab_id):
    #lab = getLabById(lab_id)
    return render_template('tmp05/lab_introduction.html')

@tmp05.route('/tmp05/contact')
def contact():
    pass