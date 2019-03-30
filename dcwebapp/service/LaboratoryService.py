#!usr/bin/python
# -*- coding: utf-8 -*-
import traceback
from dcwebapp.model.models import db, Laboratory


# 分页查询
def getLaboratoryByPage(page_index,per_page):
    pagination = Laboratory.query.paginate(page_index, per_page, error_out=False)
    labs = pagination.items
    return pagination,labs

# 根据ID获取Lab对象
def getLabById(pid):
    return Laboratory.query.filter(Laboratory.id == pid).one()

# 增加
def addLab(lab):
    try:
        db.session.add(lab)
        db.session.commit()
    except:
        traceback.print_exc()
        return False
    return True

# 修改
def updateLab(lab_id, name, intro):
    lab = getLabById(lab_id)
    lab.name = name
    lab.introduction = intro
    try:
        db.session.add(lab)
        db.session.commit()
    except:
        traceback.print_exc()
        return False
    return True

# 删除
def delLabById(lab_id):
    lab = getLabById(lab_id)
    try:
        db.session.delete(lab)
        db.session.commit()
    except:
        traceback.print_exc()
        return False
    return True
