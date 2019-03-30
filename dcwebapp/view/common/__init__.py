#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

common= Blueprint('common', __name__, template_folder='../../../templates')

from . import views