#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

back = Blueprint('back', __name__, template_folder='../../../templates')

from . import views
