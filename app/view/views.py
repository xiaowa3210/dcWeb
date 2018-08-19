#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, session, g
from app.models import db, Users, Information
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
    news1=Information(title=u'first game',content='first game start',attachment='heheh')
    db.session.add(news1)
    db.session.commit()
    news2=Information(title='second',content='second game start',attachment='hhh')
    db.session.add(news2)
    db.session.commit()
    news = Information.query.order_by(Information.create_time.desc()).limit(6)
    return render_template('home.html',news=news)


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
            new_user = Users(username=username, password=generate_password_hash(password1))
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


@app.before_request
def my_before_request():
    username = session.get('username')
    if username:
        g.user = Users.query.filter(Users.username == username).first()


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'login_user': g.user}
    return {}