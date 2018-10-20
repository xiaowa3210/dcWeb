#!usr/bin/python
# -*- coding: utf-8 -*-
import traceback

from ..utils.utils import str_to_dict
from ..model.models import  nProject, db
import json

def getProjectsByPage(page_index,per_page):
    # 这个地方要用到分页查询，每次查询12页
    pagination = nProject.query.paginate(page_index, per_page, error_out=False)
    projects = pagination.items
    return pagination,projects

def getProjectById(pid):
    return nProject.query.filter(nProject.project_id == pid).one()


def getTeamInfo(project):
    teaminfo = project.member_info
    teaminfo =teaminfo.replace("\'","\"")
    teamInfoDict = str_to_dict(teaminfo)
    teammates = teamInfoDict['teammates']
    # honors = teamInfoDict['honor']
    return teammates


def addProject(project):
    try:
        db.session.add(project)
        db.session.commit()
    except:
        traceback.print_exc()
        return False
    return True
def updateProjectByID(project):
    newProject = db.session.query(nProject).filter(nProject.project_id == project.project_id).one()

    if project:
        try:
            newProject.title = project.title
            newProject.brief = project.brief
            newProject.member_info = project.member_info
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            return False
        return True
    return False

