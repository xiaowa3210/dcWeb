import traceback
from datetime import datetime
from  app.model.models import db


def addFile(file):
    try:
        db.session.add(file)
        db.session.commit()
    except:
        return False
    return True

