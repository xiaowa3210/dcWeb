#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from flask import Blueprint, redirect
from flask_login import current_user, login_required

back01 = Blueprint('back01', __name__)

from . import views, article, lab

@back01.route('/', methods=['GET'])
@login_required
def index():
    return redirect('/back01/articleList')

'''
功能测试路由，无需登陆验证
20181007
alex
'''
@back01.route('/test', methods=['POST'])
def indexTest():
    return redirect('/back01/test')

