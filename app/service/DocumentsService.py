from ..models import Document
from app import db


def getDoucumentByID(did):
    return db.session.query(Document).filter(Document.id == did).one()


def getProjectsByPage(page_index, page_size,type,*, key):

    documents = db.session.query(Document).filter(Document.type == type ).\
        limit(page_size).offset((page_index - 1) * page_size)
    return documents

