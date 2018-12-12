#!usr/bin/python
# -*- coding: utf-8 -*-

from app.model.models import nProject, Project
from app.utils.utils import str_to_dict, str_to_list


def getProjectsByPage(page_index,per_page):
    # 这个地方要用到分页查询，每次查询12页
    pagination = nProject.query.paginate(page_index, per_page, error_out=False)
    projects = pagination.items
    return pagination,projects

def getProjectById(pid):
    return Project.query.filter(nProject.project_id == pid).one()


def getTeamInfo(project):
    teaminfo = project.teaminfo
    teamInfoDict = str_to_dict(teaminfo)
    teammates = teamInfoDict['teammates']
    honors = teamInfoDict['honor']
    return teammates,honors

#对应t_project表的操作
def getProjectById_v1(pid):
    return nProject.query.filter(nProject.project_id == pid).one()


def getTeamInfo_v1(nProject):
    teaminfosStr = nProject.member_info
    teamInfos = eval(teaminfosStr)
    picsStr = nProject.ban_url
    pics = eval(picsStr)
    return teamInfos['teammates'],pics['pics']


if __name__ == '__main__':
    project = getProjectById('1543974862420')
    teaminfos = getTeamInfo(project)
    for teaminfo in teaminfos:
        print(teaminfo['name'])



