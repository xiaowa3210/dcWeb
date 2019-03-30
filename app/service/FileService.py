import traceback
from datetime import datetime

import os

from app.model.models import db
from app.model.models import Files


def addFile(file):
    try:
        db.session.add(file)
        db.session.commit()
    except:
        traceback.print_exc()
        return False
    return True

#逻辑删除文章,将删除标志位设为1
def deleteFileByID(file_id):

    file = db.session.query(Files).filter(Files.file_id == file_id).one()
    filePath = file.local_path

    if os.path.exists(filePath):
        os.remove(filePath)
    try:
        db.session.delete(file)
        db.session.commit()
    except Exception as e:
        return False
    return True
def getFileByID(file_id):
    return db.session.query(Files).filter(Files.file_id == file_id).one()


def getFilesByPage(page_index,per_page):
    pagination = Files.query.paginate(page_index, per_page, error_out=False)
    files = pagination.items
    return pagination,files