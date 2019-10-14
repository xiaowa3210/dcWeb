#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:
@file: ProjectServiceV2.py
@time: 2019/1/2
@descrition:

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃┃
            ┃ ┳┛ ┗┳ ┃
            ┃       ┻ ┃
            ┗━┓     ┏━┛
              ┃     ┗━━━┓
              ┃ 神兽保佑  ┣┓
              ┃ 永无BUG  ┏┛
              ┗┓┓┏━┳┓┏┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
import json
import uuid
from datetime import datetime

import os

import docx
from flask import url_for
from sqlalchemy import desc

from app.model.config import UPLOAD_PATH, UEDITOR_UPLOAD_PATH, UPLOAD_FILES_PATH, UPLOAD_PICS_PATH, UPLOAD_ZIP_PATH
from app.model.entity import Project, ProjectMember, ProjectAward, ProjectStatus, Files
from app import db2
from app.service.CommonService import CommonService
from app.service.FileServiceV2 import FilesService
from app.utils.ZipUtil import compress_listfiles
from app.utils.utils import mapGet
import xlwt

# from zip.ZipUtil import compress_listfiles

commonService = CommonService()
filesService = FilesService()
def addProStatus(pname, type, status,data):
    # 添加状态信息
    publisher = commonService.getCurrentUsername(1)  # todo:暂时是anonymous
    proStatus = ProjectStatus(pname, type, publisher, status)
    proStatus.pro_startTime = data['startTime']
    proStatus.major = data['major']
    if proStatus == 2:  # 如果是提交,记录提交的时间
        proStatus.submitTime = datetime.now()
    return proStatus

# 将json数据转换成项目成员,1代表学生,0代表指导老师
def json2ProMember(data, type):
    if type == 1:
        member = ProjectMember(data['name'], 1)
        member.grade = data['grade']
        member.academy = data['academy']
        member.major = data['major']
        member.number = data['number']
        member.classId = data['classId']
        return member
    else:
        member = ProjectMember(data['name'], 0)
        member.academy = data['academy']
        member.major = data['major']
        return member

# 处理获奖信息
def json2ProAward(data):
    award = ProjectAward(data['awardName'])
    award.rank = data['rank']
    return award

def storeMainPic(files):
    if len(files) > 0:
        path = UEDITOR_UPLOAD_PATH + '/pics/'
        if not os.path.exists(path):
            os.mkdir(path)
        f = files[0]
        filename = f.filename
        suffix = filename[filename.rfind('.'):]
        local_path = str(uuid.uuid1()).replace("-", "") + suffix
        f.save(path + local_path)
        return local_path,filename

# 存储上传的文件到本地，并且将文件信息写到数据库中
def storefile(files, source, source_id, type):
    if len(files) > 0:
        if type == 0:  # 0代表保存的是图片
            path = UEDITOR_UPLOAD_PATH + "/pics/"
        else:
            path = UEDITOR_UPLOAD_PATH + "/files/"

        if not os.path.exists(path):
            os.mkdir(path)
        for f in files:
            file = Files()
            file.name = f.filename
            suffix = file.name[file.name.rfind('.'):]
            local_path = str(uuid.uuid1()).replace("-", "") + suffix
            file.path = local_path
            file.source = source  # 代表新闻附件
            file.source_id = source_id
            f.save(path + local_path)  # 保存文件到本地
            filesService.addFile(file)  # 将文件信息写入到数据库

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
                award.honorLink = mapGet(a, 'honorLink')
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


    def addProjectV1(self,request):
        # 获取信息
        pname = request.form.get("pname")
        content = request.form.get("content")
        src_content = request.form.get("src_content")
        type = request.form.get("type")
        operate = request.form.get("operate")
        status = request.form.get("status")
        member = json.loads(request.form.get("members"))  # 项目成员(不包括老师)
        awardsInfo = json.loads(request.form.get("awardsInfo"))
        mainPic = request.files.getlist("mainPic")
        cerFile = request.files.getlist("certfile")

        project = Project(pname, content, type)
        project.src_content = src_content
        project.mainPic = storeMainPic(mainPic)

        # 添加项目成员，包括学生成员和指导老师
        members = project.members
        if member:
            for m in member:
                members.append(json2ProMember(m, 1))
            if awardsInfo:
                teachers = awardsInfo['teacher']
                if teachers:
                    for t in teachers:
                        members.append(json2ProMember(t, 0))

        # 添加奖项信息
        awards = project.awards
        if awardsInfo:
            award = json2ProAward(awardsInfo)
            awards.append(award)

        # 添加状态信息
        project.status = addProStatus(pname, type, status, project.mainPic)
        db2.session.add(project)
        db2.session.commit()
        storefile(cerFile, awards[0].id, 3, 0)

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
            award.honorLink = mapGet(a, 'honorLink')
            db2.session.add(award)

        # 添加状态信息
        publisher = commonService.getCurrentUsername(1)
        status = ProjectStatus(data['pname'], data['type'], publisher, data['status'])
        status.pid = pid
        status.mainPic = mainPic
        if data['status'] == 2:  # 如果是提交,记录提交的时间
            status.submitTime = datetime.now()
        db2.session.add(status)
        db2.session.commit()



    #todo:修改项目可以改为模块化修改
    def modifiedProjectV1(self,request):
        # 获取信息
        pname = request.form.get("pname")
        content = request.form.get("content")
        src_content = request.form.get("src_content")
        type = request.form.get("type")
        operate = request.form.get("operate")
        status = request.form.get("status")
        member = json.loads(request.form.get("members"))  # 项目成员(不包括老师)
        awardsInfo = json.loads(request.form.get("awardsInfo"))
        mainPic = request.files.getlist("mainPic")
        cerFile = request.files.getlist("certfile")

        pid = request.form.get['pid']

        if mainPic:
            picName = storeMainPic(mainPic)

        pass
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
    def getPublishedPro(self,page_index,count,**kw):

        # 筛选条件
        startTime = kw['startTime']
        endTime = kw['endTime']
        type = kw['type']
        major = kw['major']
        source = kw['source']

        query = ProjectStatus.query.filter(ProjectStatus.status == 3,ProjectStatus.delete_flag == 0)
        if startTime and endTime:
            query = query.filter(ProjectStatus.pro_startTime >= startTime,ProjectStatus.pro_startTime <= endTime)
        if type != -1:
            query = query.filter(ProjectStatus.type == type)
        if major != 0:
            query = query.filter(ProjectStatus.major == major)
        if source != -1:
            query = query.filter(ProjectStatus.source == source)
        pagination = query.order_by(desc(ProjectStatus.pro_startTime)).paginate(page_index, count, error_out=False)

        pros = pagination.items
        for pro in pros:

            mainPic = db2.session.query(Files).filter(Files.source_id == pro.pid,
                                                          Files.source == 1,
                                                          Files.delete_flag == 0).one()
            pro.pic = mainPic
        return pagination, pros


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
        pagination = ProjectStatus.query.filter(ProjectStatus.publisher == sid, ProjectStatus.delete_flag == 0) \
            .order_by(ProjectStatus.checkTime).paginate(page_index, per_page, error_out=False)

        pros = pagination.items
        for pro in pros:

            mainPic = db2.session.query(Files).filter(Files.source_id == pro.pid,
                                                          Files.source == 1,
                                                          Files.delete_flag == 0).one()
            pro.pic = mainPic
        return pagination, pros


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
        pagination = ProjectStatus.query.filter(ProjectStatus.status.in_([2,3,4]),ProjectStatus.delete_flag == 0).paginate(page_index, per_page, error_out=False)
        projects = pagination.items
        return pagination, projects

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
    @:param:
    @:return:
    @descrition:提交项目
    """

    def submitPro(self, pid):
        updateContent = {
            'status': 2,                     # 将其修改成未提交的状态
            'submitTime':datetime.now()
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

        pro = Project.query.filter(Project.pid == pid).one()
        mainPic = db2.session.query(Files).filter(Files.source_id == pro.pid,
                                                  Files.source == 1,
                                                  Files.delete_flag == 0).one()
        pro.pic = mainPic


        awardList = []
        awards = pro.awards
        for a in awards:
            certPics = db2.session.query(Files).filter(Files.source_id == a.id, Files.source == 2,
                                                       Files.delete_flag == 0).all()
            pics = []
            for cp in certPics:
                cpDict = {'id': cp.fid, 'url': url_for('common.image', name=cp.path)}
                pics.append(cpDict)
            a.pics = pics
            awardList.append(a)
        pro.awardList = awardList
        return pro



    """
    @:param:
    @:return:
    @descrition:根据pid得到项目信息
    """
    def getProStatusByPid(self, pid):
        return ProjectStatus.query.filter(ProjectStatus.pid == pid).one()


    # 生成project
    def getProId(self):
        project = Project("","","")
        project.src_content = ""
        project.mainPic = 'default.jpg'

        # 添加状态信息
        publisher = commonService.getCurrentUsername(1)
        status = ProjectStatus("", "", publisher, "")
        status.mainPic = project.mainPic
        status.submitTime = datetime.now()
        project.status = status
        db2.session.add(project)
        db2.session.commit()
        return project


    #添加项目
    def addPro(self,data):
        pname = data["pname"]
        content = data["content"]
        src_content = data["src_content"]
        type = data["type"]
        source = data["source"]
        project = Project(pname, content, type)
        project.src_content = src_content
        # 添加状态信息
        project.status = addProStatus(pname, type, 1,data)
        project.status.source = source
        db2.session.add(project)
        db2.session.commit()
        if 'mainPicId' in data:
            mainPicId = data['mainPicId']
            db2.session.query(Files).filter(Files.fid == mainPicId, Files.delete_flag == 0).update({
                'source_id': project.pid
            })
            db2.session.commit()
        else:
            file = Files()
            file.name = "默认图片"
            file.path = "default.jpg"
            file.source = 1
            file.source_id = project.pid
            db2.session.add(file)
            db2.session.commit()
        return project.pid

    #修改项目
    def modifyPro(self,pid,data):
        db2.session.query(Project).filter(Project.pid == pid).update({
            'pname': data["pname"],
            'type': data["type"],
            'content':data['content'],
            'src_content':data['src_content']
        })
        db2.session.query(ProjectStatus).filter(ProjectStatus.pid == pid).update({
            'pname':data["pname"],
            'type':data["type"],
            'pro_startTime':data['startTime'],
            # 'academy':data['academy'],
            'major':data['major'],
            'source':data['source']
        })
        db2.session.commit()


    #增加项目成员
    def addProMember(self,pid,data,type):
        member = json2ProMember(data,type)
        member.pid = pid
        db2.session.add(member)
        db2.session.commit()
        return member.id


    #根据id获取成员信息
    def getMember(self,mid):
        member = db2.session.query(ProjectMember).filter(ProjectMember.id == mid).one()
        db2.session.commit()
        return member

    def getaward(self,aid):
        award = db2.session.query(ProjectAward).filter(ProjectAward.id == aid).one()

        certPics = db2.session.query(Files).filter(Files.source_id == award.id,Files.source == 2, Files.delete_flag == 0).all()

        pics = []
        for cp in certPics:
            cpDict = {'id':cp.fid,'url':url_for('common.image', name=cp.path)}
        pics.append(cpDict)
        award.pics = pics

        return award

    #修改项目成员
    def modifyProMember(self,mid,data):
        db2.session.query(ProjectMember).filter(ProjectMember.id == mid).update(data)
        db2.session.commit()

    #删除项目成员
    def deleteProMember(self,mid):
        sql = 'delete from dc_project_member where id=' + str(mid)
        db2.session.execute(sql)
        db2.session.commit()



    #增加获奖信息
    def addAwardInfo(self,pid,data):
        award = json2ProAward(data)
        award.pid = pid
        db2.session.add(award)
        db2.session.commit()
        certids = data['certids']
        if certids:
            for id in certids:
                db2.session.query(Files).filter(Files.fid == id,Files.delete_flag == 0).update({
                    'source_id': award.id
                })
                db2.session.commit()
        return award.id


    #修改获奖信息
    def modifyAwardInfo(self,aid,data):
        db2.session.query(ProjectAward).filter(ProjectAward.id == aid).update(data)
        db2.session.commit()

    #删除获奖信息
    def deleteAwardInfo(self,aid):
        sql = 'delete from dc_project_award where id=' + str(aid)
        db2.session.query(Files).filter(Files.source == 2,Files.source_id == aid,Files.delete_flag == 0).update({
                    'delete_flag':1
                })
        db2.session.execute(sql)
        db2.session.commit()

    #添加图片
    def addFile(self,source_id,id):
        db2.session.query(Files).filter(Files.fid == id, Files.delete_flag == 0).update({
            'source_id': source_id
        })
        db2.session.commit()


    #修改主页图片
    def modifyPic(self,id,files):
        path,filename = storeMainPic(files)
        db2.session.query(Files).filter(Files.fid == id, Files.delete_flag == 0).update({
            'path': path,
            'name':filename
        })
        db2.session.commit()

        return path

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
            if p.status is not None and p.status.delete_flag == 1:
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


    #生成获奖信息
    def downProAwardInfo(self,startTime,endTime,academy):
        sql = "select p.pid from dc_project_status_info AS p INNER JOIN dc_project_award AS a on p.pid = a.pid"
        where = ""
        if startTime and endTime and academy != 0:
            where += ' where a.awardTime >= ' + "'" +str(startTime) + "'" + ' and a.awardTime <=' + "'" + str(
                endTime) + "'" + ' and p.academy =' + str(academy)
        elif startTime and endTime:
            where += ' where a.awardTime >= ' + str(startTime) + ' and a.awardTime <=' + str(endTime)
        elif academy != 0:
            where += ' where p.major =' + str(academy)
        sql += where
        print(sql)
        result = db2.session.execute(sql).fetchall()
        ids = [row['pid'] for row in result]
        print(ids)
        db2.session.commit()
        pros = db2.session.query(Project).filter(Project.pid.in_(ids)).all()

        files = []
        #创建一个word文档
        doc = docx.Document()
        table = doc.add_table(rows=1, cols=4, style='Table Grid')  # 创建带边框的表格
        hdr_cells = table.rows[0].cells                            # 获取第0行所有所有单元格
        hdr_cells[0].text = '项目名'
        hdr_cells[1].text = '所获奖项'
        hdr_cells[2].text = '指导老师'
        hdr_cells[3].text = '成员信息'
        for p in pros:
            cells = table.add_row().cells
            pnametext = p.pname
            fs,awardstext = formateProjectAwards(p.awards)
            files += fs
            stutext,teachertext = formateProjectMembers(p.members)
            cells[0].text = pnametext
            cells[1].text = awardstext
            cells[2].text = teachertext
            cells[3].text = stutext

        filename = str(uuid.uuid1()).replace("-", "")+".docx"
        storePath = os.path.join(UPLOAD_FILES_PATH,filename)
        doc.save(storePath)
        files.append(storePath)

        finalfilename = str(uuid.uuid1()).replace("-", "")+".zip"
        zippath = os.path.join(UPLOAD_ZIP_PATH,finalfilename)
        compress_listfiles(zippath,files)
        return finalfilename



#将ProjectMember转为字符串,并且格式化
def formateProjectMember(member):
    if member.type == 1:
        str = "姓名:"+member.name+"\n" + \
              "学院:"+member.academy+"\n"+\
              "年级:"+member.grade+"\n"+ \
              "专业:" + member.major + "\n" + \
              "学号:" + member.number + "\n" + \
              "班级:" + member.classId + "\n" + "\n"
    elif member.type == 0:
        str = "姓名:" + member.name + "\n" + \
              "学院:" + member.academy + "\n" + \
              "专业:" + member.major + "\n" + "\n"
    return str
#将ProjectMember转为字符串,并且格式化
def formateProjectMembers(members):
    stutext = ""
    teachertext = ""
    for member in members:
        if member.type == 1:
            stutext += formateProjectMember(member)
        elif member.type == 0:
            teachertext += formateProjectMember(member)
    return stutext,teachertext

# 将ProjectMember转为字符串,并且格式化
def formateProjectAward(award):

    filename,certfile = packCertPic(award.id)
    awardtext = award.awardName + "\n" + \
          str(award.rank) + "\n" + \
          str(award.awardTime) + "\n" + \
                filename
    return certfile,awardtext

# 将ProjectMember转为字符串,并且格式化
def formateProjectAwards(awards):
    files = []
    awardtext = ""
    for award in awards:
        certfile, text = formateProjectAward(award)
        awardtext += text
        files.append(certfile)
    return files,awardtext

# 将获奖证书打包成一个压缩包
def packCertPic(aid):
    certpic = filesService.getFilesBySourceIdAndSource(2, aid)
    certpicPath = [os.path.join(UPLOAD_PICS_PATH, p.path) for p in certpic]
    filename = str(uuid.uuid1()).replace("-", "") + ".zip"
    zippath = os.path.join(UPLOAD_ZIP_PATH, filename)
    compress_listfiles(zippath,certpicPath)
    return filename,zippath