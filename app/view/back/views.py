#!/user/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template

from app.view.back import back


#******************************api接口******************************#
""" 
上传新闻
"""
@back.route('/api/uploadNew')
def uploadNew():
    pass

""" 
上传文件
"""
@back.route("/api/uploadFile")
def uploadFile():
    pass

#******************************模板******************************#
""" 
审核项目
"""
@back.route("/admin/checkproject")
def checkProject():
    return render_template("back01/back/checkproject.html")

""" 
管理项目
"""
@back.route("/admin/manageProject")
def manageProject():
    return render_template("back01/back/manageProject.html")


""" 
编辑新闻
"""
@back.route("/admin/editNews")
def editNews():
    return render_template("back01/back/editNews.html")

""" 
新闻管理
"""
@back.route("/admin/manageNews")
def manageNews():
    return render_template("back01/back/manageNews.html")

""" 
修改新闻
"""
@back.route("/admin/modifiesNews")
def modifiesNews():
    return render_template("back01/back/modifiesNews.html")

""" 
资料管理
"""
@back.route("/admin/manageResource")
def manageResource():
    return render_template("back01/back/manageResource.html")


""" 
管理员人员管理
"""
@back.route("/admin/manageUser")
def manageUser():
    return render_template("back01/back/manageUser.html")



