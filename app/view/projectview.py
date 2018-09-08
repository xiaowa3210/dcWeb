#!usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template,request
from app import app
from app.service.ProjectService import *


@app.route('/project/list', methods=['GET'])
def plistView():
    #p代表页数从请求的查询字符串（request.args）中获取，默认为1
    page = request.args.get('page', 1, type=int)
    projects,pagination = getProjectsByPage(page, key="xxx", year=2018)
    return render_template('projectview/plistView.html',projects=projects,pagination=pagination)

@app.route('/project/info', methods=['GET'])
def pDetail():
    pid = request.args.get('pid',type=int)
    project = getProjectById(pid)
    return render_template('projectview/pdetail.html',project=project)
