#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

tmp05= Blueprint('tmp05', __name__)

from . import views
