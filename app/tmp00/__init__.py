#!usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

tmp00 = Blueprint('tmp00', __name__)

from . import views
