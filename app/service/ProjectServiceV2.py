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
import uuid
from datetime import datetime

import os

from app.model.config import UPLOAD_PATH
from app.model.entity import Project, ProjectMember, ProjectAward, ProjectStatus
from app import db2
from app.service.CommonService import CommonService
from app.utils.utils import mapGet
import xlwt
commonService = CommonService()
class ProjectService:
    #添加项目
    def addProject(self,data):
        operate = data['operate']
        # 项目基本信息
        if int(operate) == 0:  # 代表添加
            project = Project(data['pname'],data['content'],data['type'])
            project.src_content = data['src_content']
            mainPics = commonService.getImgPathList(mapGet(data, 'mainPic'))
            if mainPics:
                project.mainPic = mainPics[0]
            else:
                project.mainPic = 'default.jpg'
            memberlist = project.members
            awardList = project.awards
            # 项目成员
            members = data['members']
            for m in members:
                member = ProjectMember(m['name'], m['type'])
                if member.type == 1:  # 0:代表老师，1代表学生
                    member.academy = m['academy']
                    member.grade = m['grade']
                if 'brief' in m.keys():
                    member.brief = m['brief']
                memberlist.append(member)
            # 获奖信息
            awards = data['awards']
            for a in awards:
                award = ProjectAward(a['title'])
                award.awardTime = mapGet(a, 'awardTime')
                award.certPic = json.dumps(commonService.getImgPathList(mapGet(a, 'certPic')))
                award.honorLink = json.dumps(mapGet(a, 'honorLink'))
                awardList.append(award)

            # 添加状态信息
            publisher = commonService.getCurrentUsername(1)
            status = ProjectStatus(data['pname'], data['type'], publisher, data['status'])
            status.mainPic = project.mainPic
            if data['status'] == 2:  # 如果是提交,记录提交的时间
                status.submitTime = datetime.now()
            project.status = status
            db2.session.add(project)
            db2.session.commit()
        else:
            self.modifiedProject(data)


    """ 
    @:param:
    @:return:
    @descrition:修改项目
    """
    def modifiedProject(self,data):
        #更新内容
        pid = data['pid']
        mainPics = commonService.getImgPathList(mapGet(data, 'mainPic'))
        if mainPics:
            mainPic = mainPics[0]
        else:
            mainPic = 'default.jpg'
        db2.session.query(Project).filter(Project.pid == pid).update({
            'content':data['content'],
            'src_content':data['src_content'],
            'pname':data['pname'],
            'type':data['type'],
            'mainPic':mainPic
        })

        #删除奖项,成员和状态信息。
        sql1 = 'delete from dc_project_award where pid=' + str(pid)
        sql2 = 'delete from dc_project_member where pid=' + str(pid)
        sql3 = 'delete from dc_project_status_info where pid=' + str(pid)

        db2.session.execute(sql1)
        db2.session.execute(sql2)
        db2.session.execute(sql3)

        # 项目成员
        members = data['members']
        for m in members:
            member = ProjectMember(m['name'], m['type'])
            member.pid = pid
            if member.type == 1:  # 0:代表老师，1代表学生
                member.academy = m['academy']
                member.grade = m['grade']
            if 'brief' in m.keys():
                member.brief = m['brief']
            db2.session.add(member)

        # 获奖信息
        awards = data['awards']
        for a in awards:
            award = ProjectAward(a['title'])
            award.pid = pid
            award.awardTime = mapGet(a, 'awardTime')
            award.certPic = json.dumps(commonService.getImgPathList(mapGet(a, 'certPic')))
            award.honorLink = json.dumps(mapGet(a, 'honorLink'))
            db2.session.add(member)

        # 添加状态信息
        publisher = commonService.getCurrentUsername(1)
        status = ProjectStatus(data['pname'], data['type'], publisher, data['status'])
        status.pid = pid
        status.mainPic = mainPic
        if data['status'] == 2:  # 如果是提交,记录提交的时间
            status.submitTime = datetime.now()
        db2.session.add(status)
        db2.session.commit()


    """ 
    @:param:
    @:return:
    @descrition:查询项目(未分页查询)
    """
    def getProjects(self,condition):
        if condition is not None:
            projects = Project.query.filter(condition)
        else:
            projects = Project.query
        return projects

    """ 
    @:param:(page_index)->页数
            (per_page)->每页数量
            (condition)->查询条件
    @:return:
    @descrition:分页查询项目
    """
    def getProjectsByPage(self,page_index,per_page,condition):
        if condition is not None:
            pagination = ProjectStatus.query.filter(condition).paginate(page_index, per_page, error_out=False)
        else:
            pagination = ProjectStatus.query.paginate(page_index, per_page, error_out=False)
        projects = pagination.items
        return pagination, projects


    """ 
    @:param:
    @:return:
    @descrition:查询已经审核通过的项目
    """
    def getPublishedPro(self,page_index,count):
        pagination = ProjectStatus.query.filter(ProjectStatus.status == 3,ProjectStatus.delete_flag == 0)\
            .order_by(ProjectStatus.checkTime).paginate(page_index, count, error_out=False)
        return pagination, pagination.items

    """ 
    @:param:
    @:return:
    @descrition:查询待审核的项目
    """

    def getUncheckPro(self, page_index, count):
        pagination = ProjectStatus.query.filter(ProjectStatus.status == 2, ProjectStatus.delete_flag == 0) \
            .order_by(ProjectStatus.checkTime).paginate(page_index, count, error_out=False)
        return pagination,pagination.items
    """ 
    @:param:
        updateContent:更新内容
        condition:查询条件
    @:return:
    @descrition:更新项目状态
    """
    def updateProStatus(self,updateContent,condition):
        db2.session.query(ProjectStatus).filter(condition).update(updateContent)
        db2.session.commit()


    """ 
    @:param:
    @:return:
    @descrition:根据学生ID得到，该学生上传的项目
    """
    def getProByStudentId(self,page_index,per_page):
        sid = commonService.getCurrentUsername(1)
        condition = (ProjectStatus.publisher == sid)
        return self.getProjectsByPage(page_index,per_page,condition)

    """ 
    @:param:
    @:return:
    @descrition:根据项目ID更新内容
    """
    def updateProStatusByPid(self,updateContent,pid):
        db2.session.query(ProjectStatus).filter(ProjectStatus.pid == pid).update(updateContent)
        db2.session.commit()
    """ 
    @:param:
    @:return:
    @descrition:得到学生已经上传了的项目(管理员只能对这部分项目进行管理)
    """
    def getUploadedProBypage(self,page_index,per_page):
        condition = (ProjectStatus.status.in_([2,3,4]),ProjectStatus.delete_flag)
        return self.getProjectsByPage(page_index,per_page,condition)

    """ 
    @:param:
    @:return:
    @descrition:逻辑删除项目。
    """
    def deletePro(self,pid):
        updateContent = {
            "delete_flag":1
        }
        self.updateProStatusByPid(updateContent,pid)



    """ 
    @:param:
    @:return:
    @descrition:撤销项目
    """
    def undoPro(self,pid):
        updateContent = {
            'status':3,                                     #将其改成未审核态
            'undoer':commonService.getCurrentUsername(),
            'cancelTime':datetime.now()
        }
        self.updateProStatusByPid(updateContent, pid)

    """ 
    @:param:
    @:return:
    @descrition:撤销项目
    """

    def stuUndoPro(self, pid):
        updateContent = {
            'status': 1,  # 将其修改成未提交的状态
        }
        self.updateProStatusByPid(updateContent, pid)




    """ 
    @:param:operation=0代表不通过,非0代表通过。
    @:return:
    @descrition:审核项目
    """
    def checkoutPro(self,pid,operation,msg):
        if operation == 0:
            updateContent = {
                'status': 4,
                "reviewer": commonService.getCurrentUsername(),
                "checkTime": datetime.now(),
                "msg":'审核不通过' if msg == None or msg == '' else msg
            }
        else:
            updateContent = {
                'status': 3,
                "reviewer": commonService.getCurrentUsername(),
                "checkTime": datetime.now(),
                'msg':'审核通过' if msg == None or msg == '' else msg
            }
        self.updateProStatusByPid(updateContent,pid)

    """ 
    @:param:
    @:return:
    @descrition:根据PID得到项目内容
    """
    def getProjectByID(self,pid):
        return Project.query.filter(Project.pid == pid).one()



    """ 
    @:param:
    @:return:
    @descrition:根据pid得到项目信息
    """
    def getProStatusByPid(self, pid):
        return ProjectStatus.query.filter(ProjectStatus.pid == pid).one()



    """ 
    @:param:
    @:return:
    @descrition:生成获奖信息,并写入excel
    """
    def generateAwardInfoExcel(self,condition):
        projects = self.getProjects(condition)

        f = xlwt.Workbook()

        #水平居中style
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
        style = xlwt.XFStyle()  # Create Style
        style.alignment = alignment  # Add Alignment to Style


        sheet1 = f.add_sheet('获奖信息', cell_overwrite_ok=True)
        #设置头的样式
        # 写第0行
        row0 = ["项目名", "获奖信息", "项目成员"]


        # sheet1.write(0,0,row0[0],self.set_style('Times New Roman', 220, True))
        # sheet1.write(0,1, row0[1], self.set_style('Times New Roman', 220, True))
        # sheet1.write(0, 3, row0[2], self.set_style('Times New Roman', 220, True))
        sheet1.write_merge(0, 1, 0, 0, row0[0],style)
        sheet1.write_merge(0, 0, 1, 2, row0[1],style)
        sheet1.write_merge(0, 0, 3, 6, row0[2],style)

        #写第1行
        row1 = ["所获奖项", "获奖时间", "姓名","学院","年级","类型"]
        for i in range(0, len(row1)):
            sheet1.write(1, i+1, row1[i], self.set_style('Times New Roman', 220, True))

        preX = 2
        nextX = 2
        #写入数据库中的数据
        for p in projects:
            if p.status.delete_flag == 1:
                continue
            alen = 0
            mlen = 0
            curX = preX

            # 将获奖信息写入
            curY = 1
            awards = p.awards
            tmpY = curY
            for a in awards:
                sheet1.write(curX,curY,a.awardName)#写入所获奖项
                curY += 1
                sheet1.write(curX,curY,"" if a.awardTime is None else str(a.awardTime)[0:10])#写入获奖时间
                curX += 1
                curY = tmpY
                alen += 1
            aX = curX
            nextX = nextX if curX < nextX else curX
            #将项目成员写入
            curX = preX
            curY = 3
            members = p.members
            for m in members:
                sheet1.write(curX,curY,m.name)         # 写入姓名
                curY += 1
                sheet1.write(curX,curY,m.academy)      # 写入学院
                curY += 1
                sheet1.write(curX,curY,m.grade)       # 写入年级
                curY += 1
                sheet1.write(curX,curY,"指导老师" if m.type == 0 else "学生")        # 写入类型
                curX += 1
                curY = 3
                mlen += 1
            mX = curX
            nextX = nextX if curX < nextX else curX
            # 合并单元格
            sheet1.write_merge(preX, nextX - 1, 0, 0, p.pname, self.set_style('Times New Roman', 220, True))  # 写入项目名
            if alen > mlen:
                sheet1.write_merge(mX,nextX-1,3,6)
                pass
            elif alen < mlen:
                sheet1.write_merge(aX,nextX-1,1,2)
                pass
            preX = nextX



        filename = '获奖信息'+str(uuid.uuid1()).replace("-","")+'.xls'
        f.save(os.path.join(UPLOAD_PATH, filename))
        return filename

    # 设置表格样式
    def set_style(slef,name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

