#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:
@file: ProjectServiceV2.py
@time: 2019/1/2
@descrition:

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import json
from datetime import datetime
from app.model.entity import Project, ProjectMember, ProjectAward, ProjectStatus
from app import db2
from app.service.CommonService import CommonService
from app.utils.utils import mapGet

commonService = CommonService()
class ProjectService:
    #添加项目
    def addProject(self,data):
        # 项目基本信息
        project = Project(data['pname'],data['content'],data['type'])
        project.mainPic = json.dumps(commonService.getImgPathList(mapGet(data,'certPic')))
        memberlist = project.members
        awardList = project.awards
        # 项目成员
        members = data['members']
        for m in members:
            member = ProjectMember(m['name'],m['type'])
            if member.type == 1:                                   #0:代表老师，1代表学生
                member.academy = m['academy']
                member.grade = m['grade']
            if 'brief' in m.keys():
                member.brief = m['brief']
            memberlist.append(member)
        # 获奖信息
        awards = data['awards']
        for a in awards:
            award = ProjectAward(a['title'])
            award.awardTime = mapGet(a,'awardTime')
            award.certPic = json.dumps(commonService.getImgPathList(mapGet(a,'certPic')))
            award.honorLink = json.dumps(mapGet(a,'honorLink'))
            awardList.append(award)

        #添加状态信息
        status = ProjectStatus(data['pname'],data['type'],'xiaoming',data['status'])
        if data['status'] == 2:                             #如果是提交,记录提交的时间
            status.submitTime = datetime.now()
        project.status = status
        #添加到数据库中
        db2.session.add(project)
        db2.session.commit()





