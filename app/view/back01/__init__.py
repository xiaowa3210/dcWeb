#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required

back01 = Blueprint('back01', __name__)

from . import views, article

@back01.route('/', methods=['GET'])
@login_required
def index():
    return render_template('back01/index01.html', current_user=current_user)
'''
功能测试路由，无需登陆验证
20181007
alex
'''
@back01.route('/test', methods=['POST'])
def indexTest():
    return redirect('/back01/test')

