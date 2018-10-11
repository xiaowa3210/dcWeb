#!usr/bin/python
# -*- coding: utf-8 -*-
from ..model.models import Document, Article, Files
from app import db
#type=0 代表常用下载 type=1 代表新闻公告


def getDoucumentByID(did):
    return db.session.query(Document).filter(Document.id == did).one()


def getDocumentByPage(page_index, per_page,type):
    pagination = Document.query.filter(Document.type == type).order_by(Document.created_time.desc()).paginate(page_index, per_page)
    documents = pagination.items
    return pagination,documents
def getAiticleByPage(page_index, per_page):
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(page_index, per_page)
    documents = pagination.items
    return pagination,documents
def getAiticleByID(did):
    return db.session.query(Article).filter(Article.article_id == did).one()
def getDownlinkByPage(page_index, per_page):
    pagination = Files.query.paginate(page_index, per_page)
    documents = pagination.items
    return pagination,documents
