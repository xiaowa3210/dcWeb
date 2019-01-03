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

class ProjectService:
    #添加项目
    def addProject(self,data):
        # 项目基本信息
        project = Project()
        project.pname = data['pname']
        project.type = data['type']
        project.content = data['content']
        project.mainPic = json.dumps(data['picUrl'])
        memberlist = project.members
        awardList = project.awards
        # 项目成员
        members = data['members']
        for m in members:
            member = ProjectMember()
            member.name = m['name']
            member.type = m['type']
            if member.type == 1:                                   #0:代表老师，1代表学生
                member.academy = m['academy']
                member.grade = m['grade']
            if 'brief' in m.keys():
                member.brief = m['brief']
            memberlist.append(member)
        # 获奖信息
        awards = data['awards']
        for a in awards:
            award = ProjectAward()
            award.awardName = a['title']
            award.awardTime = a['time']
            award.certPic = json.dumps(a['certPic'])
            award.honorLink = json.dumps(a['honorLink'])
            awardList.append(award)

        #添加状态信息
        status = ProjectStatus()
        status.pname = data['pname']
        status.type = data['type']
        status.status = data['status']                      #1:未提交(保存),2审核中(提交)
        if data['status'] == 2:                             #如果是提交记录提交的时间
            status.submitTime = datetime.now()
        status.publisher = 'xiaoming'
        project.status = status
        #添加到数据库中
        db2.session.add(project)
        db2.session.commit()






