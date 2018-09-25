#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

tmp02= Blueprint('tmp02', __name__)

from . import views
