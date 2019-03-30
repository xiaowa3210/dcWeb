#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

tmp01= Blueprint('tmp01', __name__, template_folder='../../../templates')

from . import views
