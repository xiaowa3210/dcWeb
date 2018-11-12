from flask import render_template, json, jsonify, request
from flask_login import login_required

from app.model.models import db, Laboratory
from app.view.back01 import back01
from app.service.LaboratoryService import *


@back01.route('/lab', methods=['GET'], defaults={'page': 1})
@back01.route('/lab/<int:page>', methods=['GET'])
@login_required
def lab(page):
    pagination, labs = getLaboratoryByPage(page, 10)
    return render_template('back01/lab.html', labs=labs, pagination=pagination)


@back01.route('/lab/create')
@login_required
def lab_create():
    return render_template('back01/lab_create.html')


@back01.route('/lab/create', methods=['POST'])
@login_required
def api_create():
    data = json.loads(request.get_data("utf-8"))
    name = data['name']
    intros = data['intros']

    lab = Laboratory(name=name, introduction=intros)
    if addLab(lab):
        return jsonify({"info": "添加成功"})
    else:
        return jsonify({"info": "添加失败"})


@back01.route('/lab/<lab_id>')
@login_required
def lab_detail(lab_id):
    lab = getLabById(lab_id)
    return render_template('back01/lab_detail.html', lab=lab)


@back01.route('/update/<int:lab_id>')
@login_required
def lab_update(lab_id):
    lab = getLabById(lab_id)
    return render_template('back01/lab_update.html',lab=lab)


@back01.route('/lab/update', methods=['POST'])
@login_required
def api_update():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    name = data['name']
    intros = data['intros']

    if updateLab(id, name, intros):
        return jsonify({"info": "修改成功"})
    else:
        return jsonify({"info": "修改失败"})


@back01.route('/lab/delete',methods=['POST'])
@login_required
def api_delete():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    if delLabById(id):
        return jsonify({"info": "删除成功"})
    else:
        return jsonify({"info": "删除失败"})

"""
************************
"""
#
# @back01.route('/deluser',methods=['POST'])
# @login_required
# def deluser():
#     id = json.loads(request.get_data("utf-8"))
#     print("*********************************")
#     print(id)
#     print("*********************************")
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'code':200,'message':'删除成功！'})

