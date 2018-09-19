#!usr/bin/python
# -*- coding: utf-8 -*-
from ..models import Document
from app import db
#type=0 代表常用下载 type=1 代表新闻公告


def getDoucumentByID(did):
    return db.session.query(Document).filter(Document.id == did).one()


def getDocumentByPage(page_index, per_page,type):
    pagination = Document.query.filter(Document.type == type).order_by(Document.created_time.desc()).paginate(page_index, per_page)
    documents = pagination.items
    return pagination,documents


