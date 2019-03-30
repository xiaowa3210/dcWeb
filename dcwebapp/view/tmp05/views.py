#!/user/bin/env python
# -*- coding:utf-8 -*-
import json
import os
from flask import render_template, make_response, send_from_directory, send_file, request, url_for, jsonify, Response

from dcwebapp.model.config import UEDITOR_UPLOAD_PATH
from dcwebapp.service.ArticleService import *
from dcwebapp.service.DocumentsService import *
from dcwebapp.service.FileService import getFileByID,getFilesByPage
from dcwebapp.service.ProjectService import *
from dcwebapp.view.MessageInfo import MessageInfo
from dcwebapp.view.tmp05 import tmp05
from dcwebapp.service.UserServiceV2 import *

from dcwebapp import app


# @tmp05.route('/')
# def home():
#     # documents = Document.query.order_by(Document.created_time.desc()).limit(6)
#     # projects = Project.query.order_by(Project.create_time.desc()).limit(3)
#     return render_template('tmp05/home.html')

@tmp05.route('/tmp05/login')
def login():
    pass

@tmp05.route('/tmp05/register')
def register():
    pass

@tmp05.route('/tmp05/logout')
def logout():
    pass

@tmp05.route('/tmp05/user')
def user_center():
    pass

@tmp05.route('/tmp05/news', defaults={'page':1})
@tmp05.route('/tmp05/news/<int:page>')
def news(page):
    per_page = 10
    articles,pagination = getArticlesByPage(page,per_page,0)
    return render_template('tmp05/news.html', pagination=pagination, articles=articles)

@tmp05.route('/tmp05/newsapi')
def newsapi(): return render_template('tmp05/newsAPI.html')

@tmp05.route('/tmp05/newsDetail/<news_id>')
def news_detail(news_id):
    article = getArticleByID(news_id)
    return render_template('tmp05/news-detail.html', article=article)

@tmp05.route('/tmp05/downlink', defaults={'page':1})
@tmp05.route('/tmp05/downlink/<int:page>')
def downlink(page):
    per_page = 10
    pagination, documents = getDocumentByPage(page, per_page, 0)
    return render_template('tmp05/downlink.html', pagination=pagination, documents=documents)

#文件下载
@tmp05.route('/tmp05/download/<string:filename>', methods=['GET'])
def download_file(filename):
    #需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(app.root_path, 'view/admin/uploads')
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


#附件下载
@tmp05.route('/tmp05/loadattachment/<string:file_id>', methods=['GET'])
def download_attachment(file_id):
    #需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    file = getFileByID(file_id)
    filename = file.local_name
    response = make_response(send_file(file.local_path))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@tmp05.route('/tmp05/projects', defaults={'page':1})
@tmp05.route('/tmp05/projects/<int:page>')
def projects(page):
    per_page = 3
    pagination,projects = getProjectsByPage(page,per_page)
    return render_template('tmp05/projects.html', pagination=pagination, projects=projects)

@tmp05.route('/tmp05/projectdetail/<project_id>')
def projects_detail(project_id):
    project_obj = getProjectById(project_id)
    teammates,honors = getTeamInfo(project_obj)
    return render_template('tmp05/projects-detail.html',
                           project=project_obj,
                           teammates=teammates,
                           honors=honors)

@tmp05.route('/tmp05/laboratorys', defaults={'page':1})
@tmp05.route('/tmp05/laboratorys/<int:page>')
def laboratorys(page):
    # per_page = 3
    # pagination,labs = getLaboratoryByPage(page,per_page)
    return render_template('tmp05/lab_introduction.html')

@tmp05.route('/tmp05/labIntroduction/<lab_id>')
def laboratoryIntroduction(lab_id):
    #lab = getLabById(lab_id)
    return render_template('tmp05/lab_introduction.html')

@tmp05.route('/tmp05/contact')
def contact():
    pass

@tmp05.route('/tmp05/pDetail03')
def projects_detail03():
    return render_template('tmp05/projects_detail03.html')


@tmp05.route('/tmp05/downlink01', defaults={'page':1})
@tmp05.route('/tmp05/downlink01/<int:page>')
def downlink01(page):
    per_page = 10
    pagination, files = getFilesByPage(page, per_page)
    return render_template('tmp05/downlink.html', pagination=pagination, files=files)

@tmp05.route('/tmp05/projects_v1', defaults={'page':1})
@tmp05.route('/tmp05/projects_v1/<int:page>')
def projects_v1(page):
    per_page = 3
    pagination,projects = getProjectsByPage(page,per_page)
    return render_template('tmp05/projects.html', pagination=pagination, projects=projects)

@tmp05.route('/tmp05/projectdetail_v1/<project_id>')
def projects_detail_v1(project_id):
    project_obj = getProjectById_v1(project_id)
    teammates,pics = getTeamInfo_v1(project_obj)
    return render_template('tmp05/projects-detail.html',
                           project=project_obj,
                           teammates=teammates,
                           pics=pics)




'''
mdeditor
'''
#测试markdown编辑器
@tmp05.route('/tmp05/mdtest')
def mdtest():
    return render_template("tmp05/mdtest.html")

# 图片上传处理
@tmp05.route('/upload/',methods=['POST'])
def upload():
    file=request.files.get('editormd-image-file')
    if not file:
        res={
            'success':0,
            'message':u'图片格式异常'
        }
    else:
        ex=os.path.splitext(file.filename)[1]#文件的后缀
        filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
        file.save(os.path.join(UEDITOR_UPLOAD_PATH,filename))
        #返回
        res={
            'success':1,
            'message':u'图片上传成功',
            'url':url_for('.image',name=filename)
        }
    return jsonify(res)

# @tmp05.route('/image/<name>')
# def image(name):
#     with open(os.path.join(UEDITOR_UPLOAD_PATH,name),'rb') as f:
#         resp=Response(f.read(),mimetype="image/jpeg")
#     return resp


@tmp05.route("/tmp05/addtest",methods=["POST"])
def addtest():
    data = json.loads(request.get_data("utf-8"))
    content = data['content']
    print(content)
    return json.dumps(MessageInfo.success(data=content).__dict__)


@tmp05.route("/tmp05/databasetest")
def databasetest():
    # user = User('dhjal', 'dakkda', 1)
    # addUser_v1(user)

    modifiedPw(66,'666666666')

    return 'hello,world'




