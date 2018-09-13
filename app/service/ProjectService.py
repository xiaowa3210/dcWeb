#!usr/bin/python
# -*- coding: utf-8 -*-
from ..models import Project

def getProjectsByPage(page, key, year):

    # 这个地方要用到分页查询，每次查询12页
    pagination = Project.query.paginate(page, per_page=9, error_out=False)
    projects = pagination.items
    return projects,pagination

def getProjectById(pid):
    return Project.query.filter(Project.id == pid).one()
