from flask import render_template,request
from app import app
from app.service.UserService import *
from app.service.ProjectService import *
@app.route('/project/list', methods=['GET'])
def plistView():
    #p代表页数从请求的查询字符串（request.args）中获取，默认为1
    page = request.args.get('page', 1, type=int)
    pagination,projects = getProjectsByPage(page, 9)
    return render_template('tmp00/plistview.html',projects=projects,pagination=pagination)

@app.route('/project/info', methods=['GET'])
def pDetail():
    pid = request.args.get('pid',type=int)
    project = getProjectById(pid)
    return render_template('tmp00/pdetail.html',project=project)


@app.route('/test', methods=['GET'])
def pTest():
    #user = addUser('xiaoxiao', '12345', 3)
    #deleteUserByUserId(5)
    # addRole('老师')
    # addRole('管理员')
    # addRole('学生')

    #flag = deleteUserByUserId(10)
    #flag = deleteUserByUsername('xiaowang')

    #flag = modifyPasswordByUserId(11,'123456789')

    #user = getUserByUsername('xiaoxiao')

    #user = getUserById(5)

    flag = addPermission('编辑','Edit')
    return "OK" + str(flag)



###
@app.route('/newtemplate/home', methods=['GET'])
def newhome():
    return render_template('newTemp/index.html')

@app.route('/newtemplate/news', methods=['GET'])
def newNews():
    return render_template('newTemp/news.html')

@app.route('/newtemplate/projects', methods=['GET'])
def newProjects():
    return render_template('newTemp/projects.html')

@app.route('/newtemplate/projectDetail', methods=['GET'])
def newProjectsDetail():
    return render_template('newTemp/projects-detail.html')

@app.route('/newtemplate/register', methods=['GET'])
def newRegister():
    return render_template('newTemp/register.html')


@app.route('/newtemplate/usercenter', methods=['GET'])
def newUserCenter():
    return render_template('newTemp/user-center.html')



