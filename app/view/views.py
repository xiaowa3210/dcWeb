#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, request, flash, redirect, url_for, session, g
from app.models import db, Users, Information
from werkzeug.security import generate_password_hash
from exts import validate_login_register, validate_change_password
from app import app


@app.route('/')
def home():
    return "hello,world"