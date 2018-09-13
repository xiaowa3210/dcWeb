#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, session, g
from app.models import db, User, Document,Project
from werkzeug.security import generate_password_hash
from exts import validate_login_register, validate_change_password
from app import app


@app.context_processor
def my_context_processor():
    user = session.get('username')
    if user:
        return {'login_user': user}
    return {}

@app.route('/')
def home():
    documents = Document.query.order_by(Document.created_time.desc()).limit(6)
    projects = Document.query.order_by(Document.created_time.desc()).limit(6)
    return render_template('home.html',documents=documents,projects=projects)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.values.get('username')
        password1 = request.values.get('password1')
        password2 = request.values.get('password2')
        message = validate_login_register(username, password1, password2)
        flash(message)
        if '成功' in message:
            new_user = User(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        message = validate_login_register(username, password)
        if '成功' in message:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('home'))
        else:
            flash(message)
            return render_template('login.html')


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/user/')
def user_center():
    return render_template('user.html')


@app.route('/user/security/', methods=['GET', 'POST'])
def security():
    if request.method == 'GET':
        return render_template('security.html')
    else:
        o_password = request.form.get('o_password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        message = validate_change_password(g.user, o_password, password1, password2)
        if '成功' in message:
            g.user.password = generate_password_hash(password1)
            db.session.commit()
            session.clear()    # 先clear再flash，否则message也会丢失
            flash(message)
            return redirect(url_for('login'))
        else:
            flash(message)
            return render_template('security.html')


@app.route('/user/user_news/', methods=['GET', 'POST'])
def user_news():
    if request.method == 'GET':
        return render_template('user_news.html')
    else:
        document_title = request.form.get('document_title')
        document_content = request.form.get('document_content')
        new_document = Document(title=document_title, content=document_content)
        db.session.add(new_document)
        db.session.commit()
        return redirect(url_for('news'))

@app.route('/news/')
def news():
    page = request.args.get('page', 1, type=int)
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page, per_page=15, error_out=False)
    documents = pagination.items
    return render_template('news.html', documents=documents, pagination=pagination)

@app.route('/new_details/<document_id>/')
def new_details(document_id):
    document_obj = Document.query.filter(Document.id == document_id).first()
    return render_template('new_details.html', document=document_obj)

@app.route('/projects/')
def projects():
    page = request.args.get('page', 1, type=int)
    pagination = Document.query.order_by(Document.created_time.desc()).paginate(page, per_page=15, error_out=False)
    documents = pagination.items
    return render_template('projects.html', projects=documents, pagination=pagination)

@app.route('/project_details/<document_id>/',methods=['GET', 'POST'])
def project_details(document_id):
    document_obj = Document.query.filter(Document.id == document_id).first()
    return render_template('project_details.html', document=document_obj)

@app.before_request
def my_before_request():
    username = session.get('username')
    if username:
        g.user = User.query.filter(User.username == username).first()


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}