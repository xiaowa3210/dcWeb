#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from ..admin import admin 


@admin.app_errorhandler(404)
def page_not_found(e):
    return render_template('back01/404.html'), 404


@admin.app_errorhandler(500)
def internal_server_error(e):
    return render_template('back01/500.html'), 500
