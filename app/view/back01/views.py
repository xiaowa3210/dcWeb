from flask import render_template
from flask_login import current_user

from app.view.back01 import back01


@back01.route('/back01', methods=['GET'])

def index():
    return render_template('back01/index01.html')

@back01.route('/back01/doucment', methods=['GET'])
def doucmentEdit():
    return render_template('back01/document_edit.html')


@back01.route('/back01/doucment01', methods=['GET'])
def doucmentEdit01():
    return render_template('back01/form_component.html')