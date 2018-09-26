#!/usr/bin/env python 
# _*_ coding: utf-8 _*_

from flask import Blueprint

tmp03 = Blueprint('tmp03', __name__)

from . import views
