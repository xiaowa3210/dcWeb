#!/user/bin/env python
# -*- coding:utf-8 -*-
import json

from flask import request

from app.service.ProjectServiceV2 import ProjectService
from app.view.MessageInfo import MessageInfo
from app.view.front import front

projectService = ProjectService()


""" 
上传项目接口
"""
@front.route('/api/uploadProject',methods=['POST'])
def uploadProject():
    #数据
    data = json.loads(request.get_data("utf-8"))
    projectService.addProject(data)
    return json.dumps(MessageInfo.success(data='保存成功').__dict__)




