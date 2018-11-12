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

def getPhotoInfo(project):
    photoinfo = project.ban_url
    photoinfo =photoinfo.replace("\'","\"")
    photoinfoDict = str_to_dict(photoinfo)
    pics = photoinfoDict['pics']
    # honors = teamInfoDict['honor']
    return pics


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
            pics=[]
            photoPaths = {"pics": pics}
            if(newProject.ban_url ==str(photoPaths)):
                newProject.ban_url = project.ban_url
            else:
                pics1 =getPhotoInfo(newProject)
                pics2 =getPhotoInfo(project)
                photoss =pics1.extend(pics2)
                photoPaths = {"pics": photoss}
                newProject.ban_url = str(photoPaths)


            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            return False
        return True
    return False

