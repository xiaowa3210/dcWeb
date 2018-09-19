#!/user/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template

from app.service.DocumentsService import *
from app.service.ProjectService import *
from app.view.tmp02 import tmp02


@tmp02.route('/tmp02')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(6)
    projects = Project.query.order_by(Project.create_time.desc()).limit(3)
    return render_template('tmp02/base.html', documents=documents, projects=projects)

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
    pagination,documents = getDocumentByPage(page,per_page,0)
    return render_template('tmp02/news.html', pagination=pagination, documents=documents)

@tmp02.route('/tmp02/news/detail/<news_id>')
def news_detail(news_id):
    news_obj = getDoucumentByID(news_id)
    return render_template('tmp02/news-detail.html', news=news_obj)

@tmp02.route('/tmp02/downlink', defaults={'page':1})
@tmp02.route('/tmp02/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 1)
    return render_template('tmp02/downlink.html', pagination=pagination, documents=documents)

@tmp02.route('/tmp02/projects', defaults={'page':1})
@tmp02.route('/tmp02/projects/<int:page>')
def projects(page):
    per_page = 10
    pagination,projects = getProjectsByPage(page,per_page)
    return render_template('tmp02/projects.html', pagination=pagination, projects=projects, )

@tmp02.route('/tmp02/projects/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    return render_template('tmp02/projects-detail.html', project=project_obj)

@tmp02.route('/tmp02/contact')
def contact():
    pass