from flask import render_template, json, jsonify, request
from app.model.models import db, Laboratory
from app.view.back01 import back01


@back01.route('/lab')
def lab():
    labs = Laboratory.query.all()
    return render_template('back01/lab.html', labs=labs)

@back01.route('/lab/create')
def lab_create():
    return render_template('back01/lab_create.html')

@back01.route('/api/lab/create',methods=['GET','POST'])
def api_create():
    data = json.loads(request.get_data("utf-8"))
    name = data['name']
    intros = data['intros']

    lab = Laboratory(name=name, introduction=intros)
    db.session.add(lab)
    db.session.commit()

    return jsonify({"info": "添加成功"})

@back01.route('/lab/<lab_id>')
def lab_detail(lab_id):
    lab = db.session.query(Laboratory).filter(Laboratory.id == lab_id).one()
    return render_template('back01/lab_detail.html', lab=lab)

@back01.route('/update/<lab_id>')
def lab_update(lab_id):
    lab = db.session.query(Laboratory).filter(Laboratory.id == lab_id).one()
    return render_template('back01/lab_update.html',lab=lab)

@back01.route('/api/lab/update', methods=['POST'])
def api_update():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    name = data['name']
    intros = data['intros']

    lab = db.session.query(Laboratory).filter(Laboratory.id == id).one()
    Laboratory.name = name
    Laboratory.introduction = intros
    db.session.add(lab)
    db.session.commit()

    return jsonify({"info": "修改成功"})

@back01.route('/api/lab/delete',methods=['POST'])
def api_delete():
    data = json.loads(request.get_data("utf-8"))
    id = data['id']
    lab = db.session.query(Laboratory).filter(Laboratory.id == id).one()
    db.session.delete(lab)
    db.session.commit()

    return jsonify({"info": "删除成功"})
