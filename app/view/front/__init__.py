#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

front= Blueprint('front', __name__, template_folder='../../../templates')

from . import views
