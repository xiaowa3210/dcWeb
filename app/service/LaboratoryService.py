#!usr/bin/python
# -*- coding: utf-8 -*-
from app.model.models import Laboratory


def getLaboratoryByPage(page_index,per_page):
    # 这个地方要用到分页查询，每次查询12页
    pagination = Laboratory.query.paginate(page_index, per_page, error_out=False)
    labs = pagination.items
    return pagination,labs

def getLabById(pid):
    return Laboratory.query.filter(Laboratory.id == pid).one()

