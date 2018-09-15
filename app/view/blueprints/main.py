#!/user/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, request
from app.models import db, User, Document, Project

tmp01 = Blueprint('tmp01',__name__)


@tmp01.route('/tmp01')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(6)
    projects = Project.query.order_by(Project.create_time.desc()).limit(3)
    return render_template('main/home.html', documents=documents, projects=projects)

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
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page, per_page)
    documents = pagination.items
    return render_template('main/news.html', pagination=pagination, documents=documents)

@tmp01.route('/tmp01/news/detail/<news_id>')
def news_detail(news_id):
    news_obj = Document.query.filter(Document.id == news_id).first()
    return render_template('main/news-detail.html', news=news_obj)

@tmp01.route('/tmp01/downlink', defaults={'page':1})
@tmp01.route('/tmp01/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page, per_page)
    documents = pagination.items
    return render_template('main/downlink.html', pagination=pagination, documents=documents)


@tmp01.route('/tmp01/projects')
def projects():
    projects = Project.query.order_by(Project.create_time.desc()).all()
    return render_template('main/projects.html', projects=projects)

@tmp01.route('/tmp01/projects/<project_id>')
def projects_detail(project_id):
    project_obj = Project.query.filter(Project.id == project_id).first()
    return render_template('main/projects-detail.html', project=project_obj)

@tmp01.route('/tmp01/contact')
def contact():
    pass