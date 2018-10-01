#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from flask import Blueprint, redirect
from flask_login import current_user, login_required

back01= Blueprint('back01', __name__)

from . import views, document

@back01.route('/back01', methods=['GET'])
@login_required
def index():
    return redirect('back01/articleList')
