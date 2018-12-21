#!/usr/bin/env python 
# _*_ coding: utf-8 _*_


'''
出现错误时，返回信息
2018.10.01 alex create
'''
from flask import render_template
from .. import app


@app.app_errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404


@app.app_errorhandler(500)
def internal_server_error(e):
    return render_template('admin/500.html'), 500