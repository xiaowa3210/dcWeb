#!usr/bin/python
# -*- coding: utf-8 -*-
from app.utils.utils import str_to_dict
from app.model.models import Project


def getProjectsByPage(page_index,per_page):
    # 这个地方要用到分页查询，每次查询12页
    pagination = Project.query.paginate(page_index, per_page, error_out=False)
    projects = pagination.items
    return pagination,projects

def getProjectById(pid):
    return Project.query.filter(Project.id == pid).one()


def getTeamInfo(project):
    teaminfo = project.teaminfo
    teamInfoDict = str_to_dict(teaminfo)
    teammates = teamInfoDict['teammates']
    honors = teamInfoDict['honor']
    return teammates,honors

