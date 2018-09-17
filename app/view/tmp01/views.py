#!/user/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template

from app.service.DocumentsService import *
from app.service.ProjectService import *
from app.view.tmp01 import tmp01


@tmp01.route('/')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(6)
    projects = Project.query.order_by(Project.create_time.desc()).limit(3)
    return render_template('tmp01/home.html', documents=documents, projects=projects)

@tmp01.route('/tmp01/login')
def login():
    pass

@tmp01.route('/tmp01/register')
def register():
    pass

@tmp01.route('/tmp01/logout')
def logout():
    pass

@tmp01.route('/tmp01/user')
def user_center():
    pass

@tmp01.route('/tmp01/news', defaults={'page':1})
@tmp01.route('/tmp01/news/<int:page>')
def news(page):
    per_page = 10
    pagination,documents = getDocumentByPage(page,per_page,0)
    return render_template('tmp01/news.html', pagination=pagination, documents=documents)

@tmp01.route('/tmp01/news/detail/<news_id>')
def news_detail(news_id):
    news_obj = getDoucumentByID(news_id)
    return render_template('tmp01/news-detail.html', news=news_obj)

@tmp01.route('/tmp01/downlink', defaults={'page':1})
@tmp01.route('/tmp01/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 1)
    return render_template('tmp01/downlink.html', pagination=pagination, documents=documents)

@tmp01.route('/tmp01/projects', defaults={'page':1})
@tmp01.route('/tmp01/projects/<int:page>')
def projects(page):
    per_page = 10
    pagination,projects = getProjectsByPage(page,per_page)
    return render_template('tmp01/projects.html', pagination=pagination, projects=projects, )

@tmp01.route('/tmp01/projects/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    return render_template('tmp01/projects-detail.html', project=project_obj)

@tmp01.route('/tmp01/contact')
def contact():
    pass